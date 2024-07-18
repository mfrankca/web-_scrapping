import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import os
import boto3
from io import BytesIO
import base64
from utility_functions import get_base64_of_bin_file, build_markup_for_logo, add_logo
def upload_file_ui():
    """
    Streamlit UI component for uploading a file.
    Supports Excel and CSV file formats.
    Returns a pandas DataFrame if a file is successfully uploaded and None otherwise.
    """
    # Allow user to select the file type
    file_type = st.selectbox("Select file type", ["Excel", "CSV"])
    
    # Define the allowed file types for the uploader based on the user's selection
    allowed_types = ["xlsx", "xls"] if file_type == "Excel" else ["csv"]
    
    # Create a file uploader widget
    uploaded_file = st.file_uploader("Upload your file", type=allowed_types)
 
image_path = "uploads//logo.png"
st.sidebar.image(image_path, use_column_width=True)
st.title("Welcome to SunRayCity Managment")    
df = upload_file_ui()
edited_df = st.data_editor(df, num_rows="dynamic", key='customers_data_editor', use_container_width=True)
   