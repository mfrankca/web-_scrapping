import re
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from io import BytesIO

# Dictionary for countries (no specific conditions or types for Amazon)
countryDict = {
    'au': '.com.au',
    'ca': '.ca',
    'de': '.de',
    'es': '.es',
    'fr': '.fr',
    'in': '.in',
    'it': '.it',
    'jp': '.jp',
    'uk': '.co.uk',
    'us': '.com',
}

def AmazonItems(query, country='us'):
    
    if country not in countryDict:
        raise Exception('Country not supported, please use one of the following: ' + ', '.join(countryDict.keys()))
    
    soup = __GetAmazonHTML(query, country)
    data = __ParseAmazonItems(soup)
    
    return data

def __GetAmazonHTML(query, country):
    # Build the URL
    parsedQuery = urllib.parse.quote(query).replace('%20', '+')
    url = f'https://www.amazon{countryDict[country]}/s?k=' + parsedQuery
    st.write(url)
    # Get the web page HTML
    request = urllib.request.urlopen(url)
    soup = BeautifulSoup(request.read(), 'html.parser')
    st.write(url)
    return soup

def __ParseAmazonItems(soup):
    rawItems = soup.find_all('div', {'data-component-type': 's-search-result'})
    data = []

    for item in rawItems:
        
        # Get item data
        title = item.find('span', class_='a-text-normal').get_text(strip=True)
        
        try: price = __ParseRawPrice(item.find('span', class_='a-price-whole').get_text(strip=True))
        except: price = None
        
        try: shipping = __ParseRawPrice(item.find('span', class_='a-price-symbol').get_text(strip=True))
        except: shipping = 0
        
        try: condition = item.find('span', class_='a-text-bold').get_text(strip=True)
        except: condition = ""
        
        try: seller = item.find('span', class_='a-size-small a-text-secondary').get_text(strip=True)
        except: seller = ""
        
        try: soldCount = int("".join(filter(str.isdigit, item.find('span', class_='a-size-base').get_text(strip=True))))
        except: soldCount = 0
        
        try: rating = item.find('span', class_='a-icon-alt').get_text(strip=True)
        except: rating = ""
        
        url = 'https://www.amazon.com' + item.find('a', class_='a-link-normal')['href']

        itemData = {
            'title': title,
            'price': price,
            'shipping': shipping,
            'condition': condition,
            'seller': seller,
            'sold-count': soldCount,
            'rating': rating,
            'url': url
        }
        data.append(itemData)
    
    return data

def __ParseRawPrice(string):
    parsedPrice = re.search('(\d+(.\d+)?)', string.replace(',', '.'))
    if (parsedPrice):
        return float(parsedPrice.group())
    else:
        return None

import pandas as pd

def ScrapeAndSaveToExcel(query, country='us', filename='product_data.xlsx', store='ebay'):
    """
    Scrapes product data from eBay or Amazon and saves it to an Excel file.

    Args:
        query (str): The search query.
        country (str): The country code for the e-commerce site.
        filename (str): The name of the Excel file to save the data to.
        store (str): The e-commerce store ('ebay' or 'amazon').

    Returns:
        None
    """
    
    if store == 'ebay':
        # Call the eBay scraper
        items = Items(query, country)
    elif store == 'amazon':
        # Call the Amazon scraper
        items = AmazonItems(query, country)
    else:
        raise Exception('Unsupported store. Please use "ebay" or "amazon".')
    
    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(items)
    
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)
    
    st.write(f'Data saved to {filename}')
