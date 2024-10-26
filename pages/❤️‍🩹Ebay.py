import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

def scrape_dynamic_ebay_product(listing_id, ebay_site='www.ebay.com'):
    url = f'https://www.ebay.com/itm/{listing_id}'
 
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: Status code {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    product_details = {}
    
    # Attempt to capture any common fields dynamically
    # Example 1: Look for all divs with text content, filtering out empty text
    for div in soup.find_all('div'):
        # Get the div's text and its class name as a potential key
        text = div.get_text(strip=True)
        if text and len(text) > 1:
            key = ' '.join(div.get('class', []))  # use class name(s) as key if available
            product_details[key] = text
    
    # Example 2: Use span elements which are often used for labels and values
    for span in soup.find_all('span'):
        text = span.get_text(strip=True)
        if text and len(text) > 1:
            key = ' '.join(span.get('class', []))
            product_details[key] = text
    
    # Example 3: Extract metadata if available
    meta_data = soup.find_all('meta', {'property': True, 'content': True})
    for meta in meta_data:
        key = meta['property']
        value = meta['content']
        product_details[key] = value
    
    # Filter the product_details dictionary to only include useful information
    # For example, ignoring irrelevant or repetitive keys.
    
    return product_details

# Usage
listing_id = '255216996716'  # Replace with actual eBay listing ID
details = scrape_dynamic_ebay_product(listing_id)
st.write(details)
