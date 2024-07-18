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

image_path = "uploads//logo.png"
st.sidebar.image(image_path, use_column_width=True)
st.title("Welcome to SunRayCity Managment")

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