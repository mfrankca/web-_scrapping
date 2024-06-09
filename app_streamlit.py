import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import os

# Extracted web scraping logic from ebay_scrap_new_V1.2.py
def scrape_ebay(item):
    url = f'https://www.ebay.com/itm/{item}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    row = {'Listing ID': item}
    try:
         title_element = soup.find('h1', attrs={'class': 'x-item-title__mainTitle'})
         row['Title'] = title_element.text.replace('Details about', '').strip() if title_element else 'Not Available'
    except AttributeError:
          row['Title'] = 'Not Available' 
         
    # Find the div with the class 'x-sellercard-atf__info__about-seller'
    seller_div = soup.find('div', class_='x-sellercard-atf__info__about-seller')

    # Find the span with the class 'ux-textspans ux-textspans--BOLD' inside the div
    seller_span = seller_div.find('span', class_='ux-textspans ux-textspans--BOLD')

    # Extract the seller name from the span
    seller_name = seller_span.text.strip()
    row['Seller'] = seller_name
    
    try:
      #price = soup.find('div', attrs={'class': 'x-price-primary'}).find('span').text.split('$')[-1].strip()
      price = soup.find('div', attrs={'class': 'x-price-primary'}).find('span').text.strip()
    except AttributeError:
            price = 'Not Available'
    row['Price'] = price

    try:
        qty = soup.find('div', attrs={'class': 'd-quantity__availability'}).find('span').text.replace(
            'available', '').replace('More than', '').strip()
    except AttributeError:
            qty = '1'
    row['Quantity'] = qty
        

    try:
         qty_element = soup.find('div', attrs={'class': 'd-quantity__availability'})
         row['Quantity'] = qty_element.find('span').text.replace('available', '').replace('More than', '').strip() if qty_element else '1'
    except:
        row['Quantity'] = 'Not Available'
        
    # Get images
    try:
          img_container = soup.find('div', {'class': 'ux-image-carousel-container'})
          if img_container:
           img_urls = [img.get('data-zoom-src', '') for img in img_container.find_all('img')[:3]]
          else:
           img_urls = []
    except Exception as e:
          print(f"An error occurred while retrieving image URLs: {e}")
          img_urls = []

     # Handle cases where fewer than 3 images are available
    row['Image URL 1'] = img_urls[0] if len(img_urls) > 0 else ''
    row['Image URL 2'] = img_urls[1] if len(img_urls) > 1 else ''
    row['Image URL 3'] = img_urls[2] if len(img_urls) > 2 else ''
        
        
        
    # Extract information from the first table
    try:
          table = soup.find('div', attrs={'id': 'viTabs_0_is'})
          if table:
             labels = table.findAll('div', {'class': 'ux-labels-values__labels-content'})
             values = table.findAll('div', {'class': 'ux-labels-values__values-content'})
             for nth, label in enumerate(labels):
                row[label.getText()] = values[nth].getText()
          else:
                print("Table 1 not found.")
    except Exception as e:
           print(f"An error occurred while extracting information from Table 1: {e}")

        # Extract information from the second table
    try:
           table1 = soup.find('div', attrs={'class': 'ux-layout-section-module'})
           if table1:
              labels = table1.findAll('div', {'class': 'ux-labels-values__labels-content'})
              values = table1.findAll('div', {'class': 'ux-labels-values__values-content'})
              for nth, label in enumerate(labels):
                 row[label.getText()] = values[nth].getText()
           else:
             print("Table 2 not found.")
    except Exception as e:
              print(f"An error occurred while extracting information from Table 2: {e}")

    return row
    # Example of data extraction
    ####title = soup.find('h1', {'class': 'it-ttl'}).text.strip() if soup.find('h1', {'class': 'it-ttl'}) else "N/A"
    ###price = soup.find('span', {'class': 'notranslate'}).text.strip() if soup.find('span', {'class': 'notranslate'}) else "N/A"
    
    return {
        'listing_id': item,
        'title': title,
        'price': price,
        'Seller':seller_name,
        'Quantity' :qty
    }

def perform_web_scraping(input_filepath):
    # Determine the file type and read the data accordingly
    _, file_extension = os.path.splitext(input_filepath)
    
    if file_extension == '.csv':
        listings = pd.read_csv(input_filepath)
    elif file_extension == '.txt':
        listings = pd.read_csv(input_filepath, header=None, names=['item'])
    else:
        st.error("Unsupported file type. Please upload a CSV or TXT file.")
        return []

    data = []
    for item in listings['item']:
        item_data = scrape_ebay(item)
        data.append(item_data)

    return data

def generate_output_files(data, output_format):
    output_files = []
    df = pd.DataFrame(data)

    if 'Excel' in output_format or 'Both' in output_format:
        excel_file = 'output.xlsx'
        df.to_excel(excel_file, index=False)
        output_files.append(excel_file)
    if 'JSON' in output_format or 'Both' in output_format:
        json_file = 'output.json'
        df.to_json(json_file, orient='records')
        output_files.append(json_file)

    return output_files

st.title('Web Scraping App')
st.write('Upload a file with listing numbers and select the output file format.')

uploaded_file = st.file_uploader('Choose a file', type=['csv', 'txt'])
output_format = st.multiselect('Select output format', ['Excel', 'JSON', 'Both'])

if uploaded_file is not None:
    if st.button('Scrape Data'):
        # Save uploaded file temporarily
        input_filepath = os.path.join('temp', uploaded_file.name)
        with open(input_filepath, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Perform web scraping
        data = perform_web_scraping(input_filepath)

        if data:
            # Generate output files
            output_files = generate_output_files(data, output_format)

            st.success('Scraping and file generation completed successfully!')

            for file in output_files:
                with open(file, 'rb') as f:
                    btn = st.download_button(
                        label=f"Download {file}",
                        data=f,
                        file_name=file,
                        mime='application/octet-stream'
                    )

if not os.path.exists('temp'):
    os.makedirs('temp')
