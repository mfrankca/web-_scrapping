import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import os
import boto3
from io import BytesIO
import base64

# Sidebar image
image_path = "uploads/logo.png"
if os.path.exists(image_path):
    st.sidebar.image(image_path, use_column_width=True)
else:
    st.sidebar.write("Logo not found")

    with st.sidebar.expander("Documentation", icon="📚"):
        st.write("""
        **Welcome to the SunRayCity Management Tool**

        ### About SunRayCity Sunglasses
        At SunRayCity Sunglasses, we search the world for the best deals on fashion and sport sunglasses. We only sell authentic and brand name sunglasses. If you are searching for a specific model that you cannot find on the site, send us an email at [sales@sunraycity.com](mailto:sales@sunraycity.com) and we will do our best to find it. We operate online only to offer these deals.

        ### Features
        - **Manage Customers**: Keep track of customer details and interactions.
        - **Product Catalog Management**: Maintain and update the product catalog.
        - **eBay Product Catalog Scraping**: Scrape product data from eBay.
        - **Scrape eBay Reviews**: Scrape reviews from the following eBay feedback pages:
          - [SunRayCity eBay Store 1](https://www.ebay.com/fdbk/feedback_profile/sunraycity)
          - [SunRayCity eBay Store 2](https://www.ebay.com/fdbk/feedback_profile/sunraycity_store)
        - **Compare Product Catalogs**: Compare the product catalog on eBay vs. the SunRayCity website.

        ### Instructions
        1. **Choose Site**: Select which eBay feedback site to scrape.
        2. **Enter URL**: Provide the URL of the eBay feedback page.
        3. **Scrape Data**: Click "Scrape Data" to collect and save reviews.

        Supported feedback sites: **eBay Feedback Site 1**, **eBay Feedback Site 2**.
        """)

def compare_catalogs(file1, file2, file_type):

    if file1 and file2:
        # Step 2: File Handling and Comparison
        st.write(file_type)
    
        if file_type == 'CSV':
            df1 = pd.read_csv(file1)
            df2 = pd.read_csv(file2)
        else:
            df1 = pd.read_excel(file1)
            df2 = pd.read_excel(file2)
    # Identify deleted and new entries based on 'Listing ID'
    deleted_entries = df2[~df2.index.isin(df1.index)]
    new_entries = df1[~df1.index.isin(df2.index)]
    
    # Compare existing entries
    df1_common = df1[df1.index.isin(df2.index)]
    df2_common = df2[df2.index.isin(df1.index)]
    
    # Align indexes and columns
    df1_common = df1_common.sort_index()
    df2_common = df2_common.sort_index()
    
    # Initialize an empty DataFrame for differences
    differences = pd.DataFrame()
    
    if 'Listing ID' not in df1.columns or 'Listing ID' not in df2.columns:
        st.error('Both files must contain the "Listing ID" column')
        return None

      # Merge DataFrames on 'Listing ID'
    merged_df = pd.merge(df1, df2, on='Listing ID', suffixes=('_file1', '_file2'))

    # Debug: Display column names after merge
    st.write("Merged DataFrame Columns:", merged_df.columns)

    # Initialize list to collect rows with differences
    diff_rows = []

    # Iterate over each row in the merged DataFrame
    for index, row in merged_df.iterrows():
        differences = []
        diff_row = {'Listing ID': row['Listing ID']}
        for col in df1.columns:
            if col != 'Listing ID':
                col_file1 = f'{col}_file1'
                col_file2 = f'{col}_file2'
                if row[col_file1] != row[col_file2]:
                    differences.append(col)
                    diff_row[col] = f"{row[col_file1]} != {row[col_file2]}"
                else:
                    diff_row[col] = row[col_file1]
        if differences:
            diff_row['Differences'] = ', '.join(differences)
            diff_rows.append(diff_row)

    # Create a DataFrame from the list of rows with differences
    diff_df = pd.DataFrame(diff_rows)
    
    st.write(diff_df.head())
  
    #except Exception as e:
     #     print(f"An error occurred while retrieving image URLs: {e}")
        
    # Return the new, deleted, and differences DataFrames, resetting index for new and deleted to include 'Listing ID'
    return new_entries.reset_index(), deleted_entries.reset_index(), diff_df

def save_comparison_result(new_entries, deleted_entries, differences, add_output_file, delete_output_file, diff_output_file):
#def save_comparison_result(new_entries, deleted_entries,  add_output_file, delete_output_file):

    new_entries.to_csv(add_output_file, index=False)
    deleted_entries.to_csv(delete_output_file, index=False)
    differences.to_csv(diff_output_file, index=False)

def main():  
    # Main title and description
    st.title("Welcome to SunRayCity Management")
    st.header('Comparfe Ebay Product Catalogs')

        
    file_type = st.selectbox("Select file type", ["Excel", "CSV","JSON"])
            
    file1 = st.file_uploader("Upload first file", type=['xlsx', 'json', 'csv'] if file_type == 'Excel' else ['json', 'csv'])
    file2 = st.file_uploader("Upload second file", type=['xlsx', 'json', 'csv'] if file_type == 'Excel' else ['json', 'csv'])

    if file1 and file2:
        new_entries, deleted_entries, differences = compare_catalogs(file1, file2, file_type)
        add_output_file = "new_entries_result.csv"
        delete_output_file = "delete_entries_result.csv"
        diff_output_file = "differences_result.csv"
        save_comparison_result(new_entries, deleted_entries, differences, add_output_file, delete_output_file, diff_output_file)
        st.success("Comparison complete! Download the result below.")
        st.download_button("Download added products", data=open(add_output_file, "rb").read(), file_name=add_output_file)
        st.download_button("Download deleted products", data=open(delete_output_file, "rb").read(), file_name=delete_output_file)
        #if differences is not None and not differences.empty:
        diff_output_file = "differences_result.csv"
            
        #save_comparison_result(new_entries, deleted_entries, add_output_file, delete_output_file)
            
        st.download_button("Download differences", data=open(diff_output_file, "rb").read(), file_name=diff_output_file)
        ##elif differences is not None and differences.empty:
        #    st.write('No differences found.')
    
if __name__ == "__main__":
    main()       