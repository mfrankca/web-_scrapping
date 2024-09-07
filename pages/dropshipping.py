import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st

def upload_file_ui():
    """
    Streamlit UI component for uploading a file.
    
    This function provides an interface for users to upload either an Excel or CSV file. 
    It supports 'xlsx', 'xls', and 'csv' file formats based on the user's selection.
    
    Returns:
        pd.DataFrame or None: A pandas DataFrame if a file is successfully uploaded and parsed, 
                              None otherwise.
    """
    # Allow user to select the file type
    file_type = st.selectbox("Select file type", ["Excel", "CSV"])
    
    # Define the allowed file types for the uploader based on the user's selection
    allowed_types = ["xlsx", "xls"] if file_type == "Excel" else ["csv"]
    
    # Create a file uploader widget
    uploaded_file = st.file_uploader("Upload your file", type=allowed_types)
    
    # Process the uploaded file if available
    if uploaded_file is not None:
        if file_type == "Excel":
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        return df
    return None

# Load the Excel file
#file_path = 'your_file.xlsx'  # Update with your file path
df = upload_file_ui()

# Function to parse HTML and extract data
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = {}
    
    # Find all <li> elements
    for li in soup.find_all('li'):
        text = li.get_text()
        # Split by the delimiter " - " to separate the key and value
        if ' - ' in text:
            key, value = text.split(' - ', 1)
            data[key.strip()] = value.strip()
    
    # Add any additional details from the <p> or <em> tags if needed
    em_text = soup.find('em')
    if em_text:
        data['Note'] = em_text.get_text().strip()
    
    return data

# Parse the HTML content in the 'Description (HTML)' column
parsed_data = df['Description (HTML)'].apply(parse_html)

# Create a DataFrame from the parsed data
parsed_df = pd.json_normalize(parsed_data)

# Combine the original DataFrame with the parsed data
result_df = pd.concat([df, parsed_df], axis=1)

# Save the result to a new Excel file
output_file_path = 'parsed_output.xlsx'  # Update with your desired output file path
result_df.to_excel(output_file_path, index=False)

st.write(f'Parsed data saved to {output_file_path}')
