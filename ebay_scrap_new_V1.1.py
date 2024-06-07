import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import sys

# Initialize a session for making HTTP requests
session = requests.Session()

# Define a function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Scrape eBay product information based on listing IDs.")
    parser.add_argument("input_file", help="Path to the input file containing eBay listing IDs")
    parser.add_argument("output_excel_file", help="Path to the output Excel file")
    parser.add_argument("output_json_file", help="Path to the output JSON file")
    return parser.parse_args()

# Define a function to scrape eBay product information
def scrape(item):
    try:
       #header = {
        #    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        #}
        header={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.9',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Model':'""',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'none',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        url = 'https://www.ebay.com/itm/' + str(item).strip()
        print('Scraping ' + str(item).strip())
        r = session.get(url, headers=header, timeout=20)
        r.raise_for_status()  # Raise an exception for bad response status
        soup = BeautifulSoup(r.content, 'html.parser')
        row = {}
        row['Listing ID'] = item.strip()
        #row['Title'] = soup.find('h1', attrs={'class': 'x-item-title__mainTitle'}).text.replace('Details about', '').strip()
        #row['Price'] = soup.find('div', attrs={'class': 'x-price-primary'}).find('span').text.split('$')[-1].strip()
        try:
            title = soup.find('h1', attrs={'class': 'x-item-title__mainTitle'}).text.replace('Details about', '').strip()  
        except AttributeError:
            title = 'Not Available'
        row['Title'] = title

        try:
            price = soup.find('div', attrs={'class': 'x-price-primary'}).find('span').text.split('$')[-1].strip()
           
        except AttributeError:
            price = 'Not Available'
        row['Price'] = price
        
        try:
            seller = soup.find('div', attrs={'class': 'ux-seller-section__item--seller'}).find('span',
                                                                                                  attrs={'class': 'ux-textspans--BOLD'}).text.strip()
        except AttributeError:
            seller = 'Not Available'
        row['Seller'] = seller
        
        try:
           shipping_message =soup.find('div',attrs={'class': 'x-shipping-message'}).find.strip()
        except AttributeError:
            shipping_message = 'Not Available'
        row['shipping Message'] = shipping_message
        
  
        try:
            qty = soup.find('div', attrs={'class': 'd-quantity__availability'}).find('span').text.replace(
                'available', '').replace('More than', '').strip()
        except AttributeError:
            qty = '1'
        row['Quantity'] = qty
         # Extract quantity information more efficiently
        try:
            qty = soup.find('div', attrs={'class': 'd-quantity__availability'}).find('span').text.replace('available', '').replace('More than', '').strip()
        except AttributeError:
            qty = '1'

        row['Quantity'] = qty
        
        #get images    
        img_urls = [img.get('data-zoom-src', '') for img in
                    soup.find('div', {'class': 'ux-image-carousel-container'}).find_all('img')[:3]]
        # Handle cases where fewer than 3 images are available
        row['Image URL 1'] = img_urls[0] if len(img_urls) > 0 else ''
        row['Image URL 2'] = img_urls[1] if len(img_urls) > 1 else ''
        row['Image URL 3'] = img_urls[2] if len(img_urls) > 2 else ''
        
        table = soup.find('div',attrs={'id':'viTabs_0_is'})
        labels = table.findAll('div', {'class': 'ux-labels-values__labels-content'})
        values = table.findAll('div', {'class': 'ux-labels-values__values-content'})
        for nth, label in enumerate(labels):
            row[label.getText()] = values[nth].getText()
           
        return row
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for item {item}: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while scraping item {item}: {e}")
        return None


# Define a function to read eBay listing IDs from the input file
def read_listing_ids(input_file):
    try:
        with open(input_file, 'r') as f:
            data = f.read().splitlines()
        return data
    except FileNotFoundError:
        print(f"Input file '{input_file}' not found.")
        sys.exit(1)

# Define a function to write scraped data to an Excel file
def write_to_excel(data, output_file):
    try:
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
        print(f"Scraped data saved to '{output_file}'.")
    except Exception as e:
        print(f"An error occurred while writing to '{output_file}': {e}")

# Define a function to write scraped data to a JSON file
def write_to_json(data, output_file):
    try:
        with open(output_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Scraped data saved to '{output_file}'.")
    except Exception as e:
        print(f"An error occurred while writing to '{output_file}': {e}")

# Main function to orchestrate the scraping process
def main():
    # Parse command-line arguments
    args = parse_arguments()
    input_file = args.input_file
    output_excel_file = args.output_excel_file
    output_json_file = args.output_json_file

    # Read eBay listing IDs from the input file
    listing_ids = read_listing_ids(input_file)

    # Scrape data for each listing ID
    scraped_data = []
    for item in listing_ids:
        data = scrape(item)
        if data:
            scraped_data.append(data)

    # Write scraped data to an Excel file
    write_to_excel(scraped_data, output_excel_file)

    # Write scraped data to a JSON file
    write_to_json(scraped_data, output_json_file)

if __name__ == "__main__":
    main()
