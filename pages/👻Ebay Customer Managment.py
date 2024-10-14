import streamlit as st
import pandas as pd
from io import BytesIO

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

def display_sidebar():
    """
    Display the sidebar with a logo image and documentation.
    """
    image_path = "uploads/logo.png"
    st.sidebar.image(image_path, use_column_width=True)
    
    # Documentation section in the sidebar
    with st.sidebar.expander("Documentation", icon="📚"):
        st.write("""
        **SunRayCity Management** is a web application built to manage Eyeware ecommerce store. 
        
        ### Features:
        - **File Upload**: Upload product data in Excel or CSV format.
        - **Data Editing**: Edit the product data directly within the application.
        
        ### Instructions:
        1. **Select File Type**: Choose the file type (Excel or CSV) you want to upload.
        2. **Upload File**: Click on "Upload your file" to upload your product data.
        3. **Edit Data**: Make changes to the data using the provided editor.
        
        Supported file formats: **Excel**, **CSV**.
        """)

def main():
    """
    Main function to set up the Streamlit app.
    """
    display_sidebar()
    
    st.title("Welcome to SunRayCity Management")
    st.header('Customer Managemenet')
    # Call the upload file UI function
    df = upload_file_ui()
    
    if df is not None:
        # Display the data editor for the uploaded DataFrame
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            key='customers_data_editor',
            use_container_width=True
        )
    else:
        st.write("Please upload a file to view and edit data.")

if __name__ == "__main__":
    main()
