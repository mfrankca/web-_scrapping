import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import sys
#import concurrent.futures  # For parallelizing scraping

session = requests.Session()

def parse_arguments(input_file,output_excel_file,output_json_file):
    parser = argparse.ArgumentParser(description="Scrape eBay product information based on listing IDs.")
    parser.add_argument(input_file, help="Path to the input file containing eBay listing IDs")
    parser.add_argument(output_excel_file, help="Path to the output Excel file")
    parser.add_argument(output_json_file, help="Path to the output JSON file")
    return parser.parse_args()

def scrape(item):
    try:
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
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html.parser')
        row = {'Listing ID': item.strip()}
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

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for item {item}: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while scraping item {item}: {e}")
        return None

def read_listing_ids(input_file):
    try:
        with open(input_file, 'r') as f:
             return f.read().splitlines()
    except FileNotFoundError:
        print(f"Input file '{input_file}' not found.")
        sys.exit(1)

def write_to_excel(data, output_file):
    try:
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
        print(f"Scraped data saved to '{output_file}'.")
    except Exception as e:
        print(f"An error occurred while writing to '{output_file}': {e}")

def write_to_json(data, output_file):
    try:
        with open(output_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Scraped data saved to '{output_file}'.")
    except Exception as e:
        print(f"An error occurred while writing to '{output_file}': {e}")

def main():
    args = parse_arguments()
    input_file = args.input_file
    output_excel_file = args.output_excel_file
    output_json_file = args.output_json_file

    listing_ids = read_listing_ids(input_file)
    # Scrape data for each listing ID
    scraped_data = []
    for item in listing_ids:
        data = scrape(item)
        if data:
            scraped_data.append(data)
         
    # Parallelize scraping for better performance
   # with concurrent.futures.ThreadPoolExecutor() as executor:
    #    scraped_data = list(executor.map(scrape, listing_ids))
   
    write_to_excel(scraped_data, output_excel_file)
    write_to_json(scraped_data, output_json_file)

if __name__ == "__main__":
    main()
