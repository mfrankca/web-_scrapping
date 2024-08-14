
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
import os

def scrape_amazon(item):
    url = f'https://www.amazon.com//itm/{item}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    row = {'Listing ID': item}
    page = requests.get(URL)

    # Check and print the title
    title_element = soup1.find(id='productTitle')
    if title_element:
        title = title_element.get_text(strip=True)
        st.write("Title:", title)
    else:
        st.write("Title not found")

    # Check and print the rating
    rating_element = soup1.find(id='acrCustomerReviewText')
    if rating_element:
        rating = rating_element.get_text(strip=True)
        st.write("Rating:", rating)
    else:
        st.write("Rating not found")
        

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
            item_data = scrape_amazon(item)
            data.append(item_data)

        return data
    
def generate_output_files(data, output_format):
    output_files = []
    df = pd.DataFrame(data)   
    # Convert the data to a DataFrame
    #df = pd.DataFrame([data], columns=columns_order)
    filtered_df = df[columns_order]
    
    if 'Excel' in output_format :
        excel_file = 'output.xlsx'
        filtered_df.to_excel(excel_file, index=False)
        output_files.append(excel_file)
    if 'JSON' in output_format :
        json_file = 'output.json'
        filtered_df.to_json(json_file, orient='records')
        output_files.append(json_file)
    if 'CSV' in output_format:
        csv_file = 'output.csv'
        filtered_df.to_csv(csv_file, index=False)
        output_files.append(csv_file) 

    return output_files

#image_path = "uploads//logo.png"
#st.sidebar.image(image_path, use_column_width=True)
#st.title("Welcome to SunRayCity Management")  

st.write('Upload a file with listing numbers and select the output file format.')
uploaded_file = st.file_uploader('Choose a file', type=['csv', 'txt'])
output_format = st.multiselect('Select output format', ['Excel', 'JSON', 'CSV'])

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

    
    
    
    
    
    
    
    

def __GetAmazonHTML(query, country):
    # Build the URL
    parsedQuery = urllib.parse.quote(query).replace('%20', '+')
    #url = f'https://www.amazon{countryDict[country]}/s?k=' + parsedQuery
   # Connect to Website and pull in data
    URL = 'https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3&customId=B0752XJYNL&th=1'
    st.write(url)
    # Get the web page HTML
    # Making the HTTP Request
    webpage = requests.get(URL)

    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    st.write(soup)
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
