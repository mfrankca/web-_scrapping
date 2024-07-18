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

file_type = st.selectbox("Select file type", ["Excel", "JSON"])
        
file1 = st.file_uploader("Upload first file", type=['xlsx', 'json'] if file_type == 'Excel' else ['json'])
file2 = st.file_uploader("Upload second file", type=['xlsx', 'json'] if file_type == 'Excel' else ['json'])

if file1 and file2:
    new_entries, deleted_entries = compare_catalogs(file1, file2, file_type)

    output_file = "comparison_result.xlsx"
    save_comparison_result(new_entries, deleted_entries, output_file)

    st.success(f"Comparison complete! Download the result below.")
    st.download_button("Download comparison result", data=open(output_file, "rb").read(), file_name=output_file)