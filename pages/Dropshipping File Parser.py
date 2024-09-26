import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from io import BytesIO

# Allowed file types
ALLOWED_FILE_TYPES = ['xlsx']

# Function to check file format
def is_valid_file_type(uploaded_file):
    return uploaded_file.name.split('.')[-1] in ALLOWED_FILE_TYPES

# Function to consolidate images and parse HTML description
def process_excel(file):
    try:
        # Step 1: Read the uploaded Excel file
        df = pd.read_excel(file)
        
        # Step 2: Group by products and consolidate 'Image Src'
        grouped_df = df.groupby('SKU').agg({
            'Title': 'first',
            'Brand': 'first',
            'Product Category': 'first',
            'Type': 'first',
            'Tags':'first',
            'Price': 'first',
            'Variant Barcode' : 'first',
            'Quantity Available': 'first',
            'Image Src': lambda x: list(x),
            'Description (HTML)': 'first'
        }).reset_index()
        
        # Step 3: Separate the images into separate columns
        grouped_df['Image URL 1'] = grouped_df['Image Src'].apply(lambda x: x[0] if len(x) > 0 else '')
        grouped_df['Image URL 2'] = grouped_df['Image Src'].apply(lambda x: x[1] if len(x) > 1 else '')
        grouped_df['Image URL 3'] = grouped_df['Image Src'].apply(lambda x: x[2] if len(x) > 2 else '')
        grouped_df = grouped_df.drop(columns=['Image Src'])
        
        # Step 4: Parse HTML from 'Description (HTML)'
        def parse_description(html):
            soup = BeautifulSoup(html, 'html.parser')
            description_dict = {}
            for li in soup.find_all('li'):
                if '-' in li.get_text():
                    key, value = li.get_text().split('-', 1)
                    key = key.strip()
                    value = value.strip()
                    description_dict[key] = value
            return description_dict

        grouped_df['Parsed Description'] = grouped_df['Description (HTML)'].apply(parse_description)
        parsed_df = grouped_df['Parsed Description'].apply(pd.Series)
        final_df = pd.concat([grouped_df.drop(columns=['Description (HTML)', 'Parsed Description']), parsed_df], axis=1)

        # Step 5: Map the columns to the expected format
        final_df['Actual Price'] = final_df['Price'] * 2
        final_df['Listing ID'] = final_df['Variant Barcode']

        # Define the columns in the expected format
        expected_columns = [
            'Listing ID', 'Title', 'Type', 'Seller', 'Price', 'Quantity',
            'Image URL 1', 'Image URL 2', 'Image URL 3',
            'Brand', 'Model','MPN','Frame Color','Frame Material', 'Style', 'Features','Lens Color', 'Lens Technology',
            'Lens Material','Department','Lens Width','Bridge Width','Vertical Height','Country/Region of Manufacture','UPC']

        # Create a new dataframe with the expected format
        output_df = pd.DataFrame(columns=expected_columns)

        # Map relevant columns
        output_df['Listing ID'] = final_df['Listing ID'] if 'Listing ID' in final_df.columns else ''
        output_df['Title'] = final_df['Title'] if 'Title' in final_df.columns else ''
        output_df['Type'] = final_df['Product Category'] if 'Product Category' in final_df.columns else ''
        output_df['Seller'] ='TeamETO'
        output_df['Brand']=final_df['Brand'] if 'Brand' in final_df.columns else ''
        output_df['Price'] = final_df['Actual Price'] if 'Actual Price' in final_df.columns else ''
        output_df['Quantity'] = final_df['Quantity Available'] if 'Quantity Available' in final_df.columns else ''
        output_df['Frame Material'] = final_df['Material'] if 'Material' in final_df.columns else ''
        output_df['Bridge Width'] = final_df['Bridge Size'] if 'Bridge Size' in final_df.columns else ''
        output_df['Features'] = final_df['Tags'] if 'Tags' in final_df.columns else ''
        output_df['Lens Color'] = final_df['Lens Colour'] if 'Lens Colour' in final_df.columns else ''
        output_df['Temple Length'] = final_df['Temple Size'] if 'Temple Size' in final_df.columns else ''
        output_df['Image URL 1'] = final_df['Image URL 1']
        output_df['Image URL 2'] = final_df['Image URL 2']
        output_df['Image URL 3'] = final_df['Image URL 3']

        return output_df

    except Exception as e:
        # Return None in case of an error
        st.error(f"An error occurred while processing the file: {str(e)}")
        return None

# Function to convert DataFrame to Excel and return BytesIO object
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output

# Streamlit App
st.title("Excel File Parser with Error Handling")

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    # Step 1: Check if the file format is valid
    if is_valid_file_type(uploaded_file):
        # Step 2: Process the uploaded Excel file
        processed_data = process_excel(uploaded_file)

        if processed_data is not None:
            # Step 3: Display the processed data
            st.write("Processed Data Preview:")
            st.dataframe(processed_data.head())

            # Step 4: Convert processed data to Excel format
            processed_excel = to_excel(processed_data)

            # Step 5: Provide download button
            st.download_button(
                label="Download Processed Excel File",
                data=processed_excel,
                file_name="processed_file.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.error("Invalid file format. Please upload an Excel file (.xlsx).")
