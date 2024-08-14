
import requests
import EbayScraper
import AmazonScraper
import streamlit as st

import streamlit as st
import pandas as pd
from io import BytesIO
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

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
# Connect to Website and pull in data
#URL = 'https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3&customId=B0752XJYNL&th=1'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

# Function to handle scraping from different e-commerce stores
def scrape_product_data(store, query, country):
    if store == 'eBay':
        return EbayScraper.Items()
    elif store == 'Amazon':
        return AmazonScraper.perform_web_scraping()
    elif store == 'Walmart':
        # Implement scraping logic for Walmart here
        pass

    return []

# Streamlit app
def main():
    st.title('Product Data Scraper')

    
    display_sidebar()

    # Dropdown to select the e-commerce store
    store = st.selectbox("Select e-commerce Store", ["eBay", "Amazon", "Walmart"])
    
    # File uploader for product descriptions
    uploaded_file = st.file_uploader("Upload a file with product descriptions", type=["csv", "xlsx"])

    # Dropdown to select the country
    #country = st.selectbox("Select Country", list(EbayScraper.countryDict.keys()))


    if uploaded_file is not None:
        # Read the uploaded file
        if uploaded_file.name.endswith('.csv'):
            product_df = pd.read_csv(uploaded_file)
        else:
            product_df = pd.read_excel(uploaded_file)
        
        st.write("Product Descriptions:")
        st.dataframe(product_df)

        # Button to start scraping
        if st.button('Scrape Product Data'):
            all_products_data = []

            for product in product_df['Product']:
                st.write(f"Scraping data for: {product}")
                product_data = scrape_product_data(store, product, country)
                all_products_data.extend(product_data)
            
            # Convert the list of dictionaries to a pandas DataFrame
            result_df = pd.DataFrame(all_products_data)

            # Save the DataFrame to an Excel file
            excel_buffer = BytesIO()
            result_df.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)

            # Download link for the Excel file
            st.download_button(
                label="Download Excel file",
                data=excel_buffer,
                file_name="product_data.xlsx",
                mime="application/vnd.ms-excel"
            )

if __name__ == '__main__':
    main()


    