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
    
    return final_df

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