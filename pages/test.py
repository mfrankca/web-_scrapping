import EbayScraper
import AmazonScraper
import streamlit as st

import streamlit as st
import pandas as pd
from io import BytesIO
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

# Assuming the scraping functions for eBay are already defined as described earlier.

# Function to handle scraping from different e-commerce stores
def scrape_product_data(store, query, country):
    if store == 'eBay':
        return EbayScraper.Items(query, country=country)
    elif store == 'Amazon':
        return AmazonScraper.AmazonItems(query, country=country)
    elif store == 'Walmart':
        # Implement scraping logic for Walmart here
        pass

    return []

# Streamlit app
def main():
    st.title('Product Data Scraper')


    # Dropdown to select the e-commerce store
    store = st.selectbox("Select e-commerce Store", ["eBay", "Amazon", "Walmart"])
    
    # File uploader for product descriptions
    uploaded_file = st.file_uploader("Upload a file with product descriptions", type=["csv", "xlsx"])

    # Dropdown to select the country
    country = st.selectbox("Select Country", list(EbayScraper.countryDict.keys()))


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
