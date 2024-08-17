import requests
import streamlit as st
import pandas as pd
from io import BytesIO
from bs4 import BeautifulSoup
import os

def scrape_ebay(item_id):
    # Implement eBay scraping logic here
    return {"Item ID": item_id, "Title": "Sample eBay Title"}

def scrape_amazon(item_id):
    # Implement Amazon scraping logic here
    return {"Item ID": item_id, "Title": "Sample Amazon Title"}

def scrape_walmart(item_id):
    # Implement Walmart scraping logic here
    return {"Item ID": item_id, "Title": "Sample Walmart Title"}

def scrape_product_data(store, item_id):
    if store == "eBay":
        return scrape_ebay(item_id)
    elif store == "Amazon":
        return scrape_amazon(item_id)
    elif store == "Walmart":
        return scrape_walmart(item_id)
    else:
        return {}

def perform_web_scraping(input_file):
    # Determine the file type and read the data accordingly
    _, file_extension = os.path.splitext(input_file.name)
    
    if file_extension == '.csv':
        listings = pd.read_csv(input_file)
    elif file_extension == '.txt':
        listings = pd.read_csv(input_file, header=None, names=['Item ID'])
    else:
        st.error("Unsupported file type. Please upload a CSV or TXT file.")
        return pd.DataFrame()

    return listings

def display_sidebar():
    """
    Display the sidebar with a logo image and documentation.
    """
    image_path = "uploads/logo.png"
    st.sidebar.image(image_path, use_column_width=True)

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

st.title('Product Data Scraper')
display_sidebar()

# Dropdown to select the e-commerce store
store = st.selectbox("Select e-commerce Store", ["eBay", "Amazon", "Walmart"])

# Upload text file with listing IDs
#uploaded_file = st.file_uploader('Choose a file (CSV or TXT)', type=['csv', 'txt'],key="listing_file_uploader")

# Output format selection
output_format = st.selectbox('Select output format', ['Excel', 'CSV'],key="output_format_selector")

if uploaded_file is not None:
    listings = perform_web_scraping(uploaded_file)
    if not listings.empty:
        st.write("Listing IDs:")
        st.dataframe(listings)

        # Button to start scraping
        if st.button('Scrape Product Data'):
            all_products_data = []
            
            for item_id in listings['Item ID']:
                st.write(f"Scraping data for: {item_id}")
                product_data = scrape_product_data(store, item_id)
                all_products_data.append(product_data)

            result_df = pd.DataFrame(all_products_data)

            if output_format == 'Excel':
                excel_buffer = BytesIO()
                result_df.to_excel(excel_buffer, index=False)
                excel_buffer.seek(0)

                st.download_button(
                    label="Download Excel file",
                    data=excel_buffer,
                    file_name="product_data.xlsx",
                    mime="application/vnd.ms-excel"
                )
            elif output_format == 'CSV':
                csv_buffer = result_df.to_csv(index=False).encode('utf-8')

                st.download_button(
                    label="Download CSV file",
                    data=csv_buffer,
                    file_name="product_data.csv",
                    mime="text/csv"
                )
