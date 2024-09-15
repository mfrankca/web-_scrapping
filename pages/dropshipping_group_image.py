import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from io import BytesIO

# Function to consolidate images and parse HTML description
def process_excel(file):
    # Read the uploaded Excel file
    df = pd.read_excel(file)
    
    # Step 1: Group by products and consolidate 'Image Src'
    grouped_df = df.groupby('SKU').agg({
        'Title': 'first',
        'Brand': 'first',
        'Product Category': 'first',
        'Type': 'first',
        'Tags':'first',
        'Price': 'first',
        'Variant Barcode' : 'first',
        'Quantity Available': 'first',
        'Image Src': lambda x: list(x),  # Aggregate images into a list
        'Description (HTML)': 'first'  # Take the first occurrence of the HTML description
    }).reset_index()
    
    # Separate the images into separate columns
    grouped_df['Image URL 1'] = grouped_df['Image Src'].apply(lambda x: x[0] if len(x) > 0 else '')
    grouped_df['Image URL 2'] = grouped_df['Image Src'].apply(lambda x: x[1] if len(x) > 1 else '')
    grouped_df['Image URL 3'] = grouped_df['Image Src'].apply(lambda x: x[2] if len(x) > 2 else '')
    
    # Drop the 'Image Src' list column as we now have separate columns
    grouped_df = grouped_df.drop(columns=['Image Src'])
    
    # Step 2: Parse HTML from 'Description (HTML)' column
      # Step 2: Parse HTML from 'Description (HTML)' column
    def parse_description(html):
        soup = BeautifulSoup(html, 'html.parser')
        description_dict = {}
        for li in soup.find_all('li'):
            if '-' in li.get_text():
                key, value = li.get_text().split('-', 1)
                key = key.strip()  # Column name
                value = value.strip()  # Column value
                description_dict[key] = value
        return description_dict
    
    # Apply the HTML parsing and create new columns for each parsed item
    grouped_df['Parsed Description'] = grouped_df['Description (HTML)'].apply(parse_description)
    
    # Expand the dictionary into separate columns
    parsed_df = grouped_df['Parsed Description'].apply(pd.Series)
    
    # Concatenate the new parsed columns with the original dataframe
    final_df = pd.concat([grouped_df.drop(columns=['Description (HTML)', 'Parsed Description']), parsed_df], axis=1)
    
     # Step 3: Map the columns to the expected format
    
    # Define the columns in the expected format
    expected_columns = [
        'Listing ID', 'Title', 'Type', 'Seller', 'Price', 'Quantity', 
        'Image URL 1', 'Image URL 2', 'Image URL 3', 
        'Brand', 'Model', 'MPN', 'Frame Color', 'Frame Material', 'Style', 
        'Features', 'Lens Color', 'Lens Technology', 'Lens Material', 'Department',
        'Lens Socket Width', 'Bridge Width', 'Vertical', 'Temple Length', 
        'Country/Region of Manufacture', 'UPC'
    ]
    
    # Create a new dataframe with the expected format
    output_df = pd.DataFrame(columns=expected_columns)
    
    # Assuming the uploaded file has relevant columns, you can map them here
    # Map relevant columns (update based on actual input file structure)
    output_df['Listing ID'] = df['UPC'] if 'UPC' in df.columns else ''
    output_df['Title'] = df['Title'] if 'Title' in df.columns else ''
    output_df['Type'] = df['Product Category'] if 'Product Category' in df.columns else ''
    output_df['Seller'] = df['Brand'] if 'Brand' in df.columns else ''
    output_df['Price'] = df['Price'] if 'Price' in df.columns else ''
    output_df['Quantity'] = df['Quantity Available'] if 'Quantity Available' in df.columns else ''
    
    # For image URLs, map them from the file if they exist, else leave blank
    output_df['Image URL 1'] = final_df['Image URL 1']
    output_df['Image URL 2'] = final_df['Image URL 2']
    output_df['Image URL 3'] = final_df['Image URL 3']
    
    # Map other relevant columns
    output_df['Brand'] = df['Brand'] if 'Brand' in df.columns else ''
    output_df['Model'] = df['Model'] if 'Model' in df.columns else ''
    output_df['MPN'] = df['MPN'] if 'MPN' in df.columns else ''
    output_df['Frame Color'] = final_df['Frame Color'] if 'Frame Color' in final_df.columns else ''
    output_df['Frame Material'] = final_df['Frame Material'] if 'Frame Material' in final_df.columns else ''
    output_df['Style'] = final_df['Style'] if 'Style' in final_df.columns else ''
    output_df['Features'] = final_df['Features'] if 'Features' in final_df.columns else ''
    output_df['Lens Color'] = final_df['Lens Color'] if 'Lens Color' in final_df.columns else ''
    output_df['Lens Technology'] = final_df['Lens Technology'] if 'Lens Technology' in final_df.columns else ''
    output_df['Lens Material'] = final_df['Lens Material'] if 'Lens Material' in final_df.columns else ''
    output_df['Department'] = final_df['Department'] if 'Department' in final_df.columns else ''
    output_df['Lens Socket Width'] = final_df['Lens Socket Width'] if 'Lens Socket Width' in final_df.columns else ''
    output_df['Bridge Width'] = final_df['Bridge Width'] if 'Bridge Width' in final_df.columns else ''
    output_df['Vertical'] = final_df['Vertical'] if 'Vertical' in final_df.columns else ''
    output_df['Temple Length'] = final_df['Temple Length'] if 'Temple Length' in final_df.columns else ''
    output_df['Country/Region of Manufacture'] = final_df['Country/Region of Manufacture'] if 'Country/Region of Manufacture' in final_df.columns else ''
    output_df['UPC'] = df['Variant Barcode'] if 'Variant Barcode' in df.columns else ''
    
    return output_df

    #return final_df

# Function to convert DataFrame to Excel and return BytesIO object
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output

# Streamlit App
st.title("Excel File Parser")

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    # Process the uploaded Excel file
    processed_data = process_excel(uploaded_file)
    
    # Display the processed data
    st.write("Processed Data Preview:")
    st.dataframe(processed_data.head())
    
    # Convert processed data to Excel format
    processed_excel = to_excel(processed_data)
    
    # Provide download button
    st.download_button(
        label="Download Processed Excel File",
        data=processed_excel,
        file_name="processed_file.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )