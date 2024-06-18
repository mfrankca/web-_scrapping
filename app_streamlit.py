
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import os
import boto3
from io import BytesIO
import base64

#st.set_page_config(layout="wide")

# Function to compare two dataframes
def compare_catalogs(file1, file2, file_type):
    if file_type == 'Excel':
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
    else:
        df1 = pd.read_json(file1)
        df2 = pd.read_json(file2)

    deleted_entries= df2[~df2['Listing ID'].isin(df1['Listing ID'])]
    new_entries  = df1[~df1['Listing ID'].isin(df2['Listing ID'])]

    return new_entries, deleted_entries
# Function to save the comparison result to an Excel file
def save_comparison_result(new_entries, deleted_entries, output_file):
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        new_entries.to_excel(writer, index=False, sheet_name='New Entries')
        deleted_entries.to_excel(writer, index=False, sheet_name='Deleted Entries')

# Extracted web scraping logic from ebay_scrap_new_V1.2.py
def scrape_ebay(item):
    url = f'https://www.ebay.com/itm/{item}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    row = {'Listing ID': item}
    try:
         title_element = soup.find('h1', attrs={'class': 'x-item-title__mainTitle'})
         row['Title'] = title_element.text.replace('Details about', '').strip() if title_element else 'Not Available'
    except AttributeError:
          row['Title'] = 'Not Available' 
         
    # Find the div with the class 'x-sellercard-atf__info__about-seller'
    seller_div = soup.find('div', class_='x-sellercard-atf__info__about-seller')

    # Find the span with the class 'ux-textspans ux-textspans--BOLD' inside the div
    seller_span = seller_div.find('span', class_='ux-textspans ux-textspans--BOLD')

    # Extract the seller name from the span
    seller_name = seller_span.text.strip()
    row['Seller'] = seller_name
    
    try:
      #price = soup.find('div', attrs={'class': 'x-price-primary'}).find('span').text.split('$')[-1].strip()
      price = soup.find('div', attrs={'class': 'x-price-primary'}).find('span').text.strip()
    except AttributeError:
            price = 'Not Available'
    row['Price'] = price

    try:
        qty = soup.find('div', attrs={'class': 'd-quantity__availability'}).find('span').text.replace(
            'available', '').replace('More than', '').strip()
    except AttributeError:
            qty = '1'
    row['Quantity'] = qty
        

    try:
         qty_element = soup.find('div', attrs={'class': 'd-quantity__availability'})
         row['Quantity'] = qty_element.find('span').text.replace('available', '').replace('More than', '').strip() if qty_element else '1'
    except:
        row['Quantity'] = 'Not Available'
        
    # Get images
    try:
          img_container = soup.find('div', {'class': 'ux-image-carousel-container'})
          if img_container:
           img_urls = [img.get('data-zoom-src', '') for img in img_container.find_all('img')[:3]]
          else:
           img_urls = []
    except Exception as e:
          print(f"An error occurred while retrieving image URLs: {e}")
          img_urls = []

     # Handle cases where fewer than 3 images are available
    row['Image URL 1'] = img_urls[0] if len(img_urls) > 0 else ''
    row['Image URL 2'] = img_urls[1] if len(img_urls) > 1 else ''
    row['Image URL 3'] = img_urls[2] if len(img_urls) > 2 else ''
        
        
        
    # Extract information from the first table
    try:
          table = soup.find('div', attrs={'id': 'viTabs_0_is'})
          if table:
             labels = table.findAll('div', {'class': 'ux-labels-values__labels-content'})
             values = table.findAll('div', {'class': 'ux-labels-values__values-content'})
             for nth, label in enumerate(labels):
                row[label.getText()] = values[nth].getText()
          else:
                print("Table 1 not found.")
    except Exception as e:
           print(f"An error occurred while extracting information from Table 1: {e}")

        # Extract information from the second table
    try:
           table1 = soup.find('div', attrs={'class': 'ux-layout-section-module'})
           if table1:
              labels = table1.findAll('div', {'class': 'ux-labels-values__labels-content'})
              values = table1.findAll('div', {'class': 'ux-labels-values__values-content'})
              for nth, label in enumerate(labels):
                 row[label.getText()] = values[nth].getText()
           else:
             print("Table 2 not found.")
    except Exception as e:
              print(f"An error occurred while extracting information from Table 2: {e}")

    return row
    # Example of data extraction
    ####title = soup.find('h1', {'class': 'it-ttl'}).text.strip() if soup.find('h1', {'class': 'it-ttl'}) else "N/A"
    ###price = soup.find('span', {'class': 'notranslate'}).text.strip() if soup.find('span', {'class': 'notranslate'}) else "N/A"
    
    return {
        'listing_id': item,
        'title': title,
        'price': price,
        'Seller':seller_name,
        'Quantity' :qty
    }

def perform_web_scraping(input_filepath):
    # Determine the file type and read the data accordingly
    _, file_extension = os.path.splitext(input_filepath)
    
    if file_extension == '.csv':
        listings = pd.read_csv(input_filepath)
    elif file_extension == '.txt':
        listings = pd.read_csv(input_filepath, header=None, names=['item'])
    else:
        st.error("Unsupported file type. Please upload a CSV or TXT file.")
        return []

    data = []
    for item in listings['item']:
        item_data = scrape_ebay(item)
        data.append(item_data)

    return data

def generate_output_files(data, output_format):
    output_files = []
    df = pd.DataFrame(data)

    if 'Excel' in output_format or 'Both' in output_format:
        excel_file = 'output.xlsx'
        df.to_excel(excel_file, index=False)
        output_files.append(excel_file)
    if 'JSON' in output_format or 'Both' in output_format:
        json_file = 'output.json'
        df.to_json(json_file, orient='records')
        output_files.append(json_file)

    return output_files


def load_colors(file=None):
    # AWS S3 configuration
    BUCKET_NAME = 'sunraycolors'
    EXCEL_FILE_KEY = 'colors.xlsx'

    # Fetch environment variables
    aws_access_key_id = st.secrets["aws_access_key_id"]
    aws_secret_access_key = st.secrets["aws_secret_access_key"]
    aws_default_region = st.secrets["aws_default_region"]
    # Initialize S3 client
    s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_default_region
)
    #st.write("DB username:", st.secrets["aws_access_key_id"])
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=EXCEL_FILE_KEY)
    df = pd.read_excel(BytesIO(response['Body'].read()), sheet_name='Colors')
    return df

# Function to get Pantone color information
def get_pantone_color(pantone_number):
    response = requests.get(f"https://connect.pantone.com//id?hex={pantone_number.lstrip('#')}")
    if response.status_code == 200:
        return response.json()
    else:
       st.error("Error fetching Pantone color information.")
       return None

def load_dataframe(uploaded_file):
    if uploaded_file.name.endswith('.json'):
        df = pd.read_json(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file format")
    return df

def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def build_markup_for_logo(
    png_file,
    background_position="50% 10%",
    margin_top="10%",
    image_width="60%",
    image_height="",
):
    binary_string = get_base64_of_bin_file(png_file)
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    background-position: %s;
                    margin-top: %s;
                    background-size: %s %s;
                }
            </style>
            """ % (
        binary_string,
        background_position,
        margin_top,
        image_width,
        image_height,
    )
def add_logo(png_file):
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )  
    
# Function to get the selected record
def get_selected_record():
    selected_rows = st.session_state["data_editor"]["selected_rows"]
    if selected_rows:
        selected_row_index = selected_rows[0]
        return edited_df.iloc[selected_row_index]
    return None   
# Streamlit application
def main():
    
    # Add logo to the sidebar

    image_path = "uploads//logo.png"
    st.sidebar.image(image_path, use_column_width=True)
    st.title("Welcome to SunRayCity Managment")
    
    # Add CSS for spacing
    st.sidebar.markdown(
        """
        <style>
        .sidebar .radio-group {
            margin-bottom: 40px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.title("Sun Ray City Managment")
    option = st.sidebar.radio("Choose an option", 
                              ["eBay Web Scraping", 
                               "Color Management", 
                               "Product Catalog Management", 
                               "Customers Management", 
                               "Compare eBay and eCommerce Product Catalogs"])

    if option == "eBay Web Scraping":
        st.header('Web Scraping App')
        st.write('Upload a file with listing numbers and select the output file format.')

        uploaded_file = st.file_uploader('Choose a file', type=['csv', 'txt'])
        output_format = st.multiselect('Select output format', ['Excel', 'JSON', 'Both'])

        if uploaded_file is not None:
            if st.button('Scrape Data'):
                # Save uploaded file temporarily
                input_filepath = os.path.join('temp', uploaded_file.name)
                with open(input_filepath, 'wb') as f:
                    f.write(uploaded_file.getbuffer())

                # Perform web scraping
                data = perform_web_scraping(input_filepath)

                if data:
                    # Generate output files
                    output_files = generate_output_files(data, output_format)

                    st.success('Scraping and file generation completed successfully!')

                    for file in output_files:
                        with open(file, 'rb') as f:
                            btn = st.download_button(
                                label=f"Download {file}",
                                data=f,
                                file_name=file,
                                mime='application/octet-stream'
                            )

        if not os.path.exists('temp'):
            os.makedirs('temp')
            
    if option == "Product Catalog Management":
        st.header('Product Catalog Management')
        st.write('Select a file to load product data.')

        uploaded_file = st.file_uploader("Choose a file", type=["json", "xlsx"])

        if uploaded_file is not None:
                    st.write('Product Data:')
                    df = load_dataframe(uploaded_file)
                    edited_df = st.data_editor(df, column_config={
        "Listing ID": st.column_config.NumberColumn(
            "Listing ID"
        ),
        
    }, num_rows="dynamic", key='product_data_editor',hide_index=None,use_container_width=True)

                    if st.button('Save Changes'):
                        if file_type == 'Excel':
                            edited_df.to_excel(file_path, index=False)
                        elif file_type == 'JSON':
                            edited_df.to_json(file_path, orient='records', indent=2)
                        st.success('Changes saved successfully!')

        #else:
         #   st.error("Invalid directory path.")
        
    elif option == "Color Management":
        st.header('Color Management')
        st.write('Loading color data from S3...')
        
        # AWS S3 configuration
        BUCKET_NAME = 'sunraycolors'
        EXCEL_FILE_KEY = 'colors.xlsx'

        df = load_colors( EXCEL_FILE_KEY)
        if df is not None:
           #st.write('Color Data:', df)

            ###edited_df = st.data_editor(df, num_rows="dynamic")
            #color_hex='FF6F61'
            edited_df=st.data_editor(
    df,num_rows="dynamic"
)
    # Initialize session state for selected rows
    if "selected_rows" not in st.session_state:  
       st.session_state["selected_rows"] = []        
            
        # Get the selected record
    selected_record = get_selected_record()

    # If a record is selected, display the hex code value
    if selected_record is not None:
       color_value = selected_record['Color']
       st.write(f'Selected Hex Code: {color_value}')
    else:
       st.write('Select a row to see the hex code value')
    
    
    
    if st.button('Save Changes'):
                with pd.ExcelWriter('updated_colors.xlsx', engine='openpyxl') as writer:
                    edited_df.to_excel(writer, index=False)
                st.success('Changes saved successfully!')
                
       
                
    elif option == "Customers Management":
           st.write("PLACEHOLDER")
    elif option == "Compare eBay and eCommerce Product Catalogs":
        file_type = st.selectbox("Select file type", ["Excel", "JSON"])
        
        file1 = st.file_uploader("Upload first file", type=['xlsx', 'json'] if file_type == 'Excel' else ['json'])
        file2 = st.file_uploader("Upload second file", type=['xlsx', 'json'] if file_type == 'Excel' else ['json'])

        if file1 and file2:
            new_entries, deleted_entries = compare_catalogs(file1, file2, file_type)

            output_file = "comparison_result.xlsx"
            save_comparison_result(new_entries, deleted_entries, output_file)

            st.success(f"Comparison complete! Download the result below.")
            st.download_button("Download comparison result", data=open(output_file, "rb").read(), file_name=output_file)

if __name__ == "__main__":
    main()
