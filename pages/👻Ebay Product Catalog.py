import streamlit as st
import pandas as pd
import os

# Sidebar image
image_path = "uploads/logo.png"
if os.path.exists(image_path):
    st.sidebar.image(image_path, use_column_width=True)
else:
    st.sidebar.write("Logo not found")

# Main title and description
st.title("Welcome to SunRayCity Management")
st.header('Product Catalog Management')
st.write('Select a file to load product data.')

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["json", "xlsx"])

def load_dataframe(uploaded_file):
    """
    Load a dataframe from the uploaded file.

    Parameters:
    uploaded_file: The uploaded file object.

    Returns:
    df: The loaded dataframe.
    """
    try:
        if uploaded_file.name.endswith('.json'):
            df = pd.read_json(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            raise ValueError("Unsupported file format")
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Process the uploaded file
if uploaded_file is not None:
    df = load_dataframe(uploaded_file)
    
    if df is not None:
        st.write('Product Data:')
        
        edited_df = st.data_editor(df, column_config={
            "Listing ID": st.column_config.NumberColumn(
                "Listing ID"
            ),
        }, num_rows="dynamic", key='product_data_editor', hide_index=None, use_container_width=True)

        # Save changes button
        if st.button('Save Changes'):
            try:
                file_type = uploaded_file.name.split('.')[-1].lower()
                if file_type == 'xlsx':
                    edited_df.to_excel(uploaded_file.name, index=False)
                elif file_type == 'json':
                    edited_df.to_json(uploaded_file.name, orient='records', indent=2)
                st.success('Changes saved successfully!')
            except Exception as e:
                st.error(f"Error saving file: {e}")
    else:
        st.error("Failed to load the uploaded file.")

# Documentation
with st.sidebar.expander("Documentation", icon="📚"):
    st.write("""
    **SunRayCity Management** is a web application built to manage Eyeware ecommerce store. 

    ### Features:
    - **File Upload**: Upload product data in JSON or Excel format.
    - **Data Editing**: Edit the product data directly within the application.
    - **Save Changes**: Save the edited data back to the original file format.

    ### Instructions:
    1. **Upload File**: Click on "Choose a file" to upload your product data.
    2. **Edit Data**: Make changes to the data using the provided editor.
    3. **Save Changes**: Click on "Save Changes" to save your edits.

    Supported file formats: **JSON**, **Excel**.
    """)
