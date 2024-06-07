import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import sys
import concurrent.futures  # For parallelizing scraping

session = requests.Session()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Scrape eBay product information based on listing IDs.")
    parser.add_argument("input_file", help="Path to the input file containing eBay listing IDs")
    parser.add_argument("output_excel_file", help="Path to the output Excel file")
    parser.add_argument("output_json_file", help="Path to the output JSON file")
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
        #row = {'Listing ID': item.strip()}
        print(soup)
        row={}
        #try:
        #title = Soup.find('h1',attrs={'class':'x-item-title__mainTitle'}).text.replace('Details about','').strip()
        #<h1 class="x-item-title__mainTitle"> <span class="ux-textspans ux-textspans--BOLD">FLEXON 472 023 Silver Lilac Eyeglasses 472-023 50mm Marchon</span></h1>
        title_tag = soup.find('h1', class_='x-item-title__mainTitle')

        # Extract the text from the span tag within the h1 tag
        if title_tag:
          title = title_tag.span.text.strip()
          print("Title:", title)
        else:
          print("Title not found.")
        #except:
        #    title = 'Not Available'
        try:
            price = Soup.find('div',attrs={'class':'x-price-primary'}).find('span').text.split('$')[-1].strip()
        except:
            price = 'Not Available'
        try:
            seller = Soup.find('div',attrs={'class':'ux-seller-section__item--seller'}).find('span',attrs={'class':'ux-textspans--BOLD'}).text.strip()
        except:
            seller = 'Not Available'

        try:
            qty=Soup.find('div',attrs={'class':'d-quantity__availability'}).find('span').text.replace('available','').replace('More than','').strip()
        except:
            qty='1'
        row['Title']=title
        row['Price']=price
        row['Quantity']=qty
        row['code']=url
        row['Seller']=seller
        img1 = ''
        img2 = ''
        img3 = ''
        try:
            # img1 = Soup.findAll('button',{'class':'image'})[0].find('img').get('src').replace('s-l64','s-l900')
            # img1 = Soup.find_all('img',{'class':'ux-image-magnify__image--original'})[0].get('data-onload-src')
            # img1 = Soup.find('div',{'class':'ux-image-carousel img-transition-medium'}).find_all('img')[0].get('data-onload-src')
            img1 = Soup.find('div',{'class':'ux-image-carousel-container'}).find_all('img')[0].get('data-zoom-src')
        except Exception as e:
            img1 = ''
        try:
            # img2 = Soup.findAll('button',{'class':'image'})[1].find('img').get('src').replace('s-l64','s-l900')
            # img2 = Soup.find_all('img',{'class':'ux-image-magnify__image--original'})[1].get('data-src')
            # img2 = Soup.find('div',{'class':'ux-image-carousel img-transition-medium'}).find_all('img')[1].get('data-src')
            img2 = Soup.find('div',{'class':'ux-image-carousel-container'}).find_all('img')[1].get('data-zoom-src')
        except:
            img2 = ''
        try:
            # img3 = Soup.findAll('button',{'class':'image'})[2].find('img').get('src').replace('s-l64','s-l900')
            # img3 = Soup.find_all('img',{'class':'ux-image-magnify__image--original'})[2].get('data-src')
            # img3 = Soup.find('div',{'class':'ux-image-carousel img-transition-medium'}).find_all('img')[2].get('data-src')
            img3 = Soup.find('div',{'class':'ux-image-carousel-container'}).find_all('img')[2].get('data-zoom-src')
        except:
            img3 = ''
        row['Image URL 1'] = img1
        row['Image URL 2'] = img2
        row['Image URL 3'] = img3
        table = Soup.find('div',attrs={'id':'viTabs_0_is'})
        labels = table.findAll('div', {'class': 'ux-labels-values__labels-content'})
        values = table.findAll('div', {'class': 'ux-labels-values__values-content'})
        for nth,label in enumerate(labels):
            row[label.getText()]=values[nth].getText()
        rows.append(row)
        return row
        # df=pd.DataFrame(rows)
        # df.to_excel('Ebay.xlsx',index=False)
    except:pass
    #except requests.exceptions.RequestException as e:
     #   print(f"Error fetching data for item {item}: {e}")
      #  return None
    #except Exception as e:
     #   print(f"An error occurred while scraping item {item}: {e}")
      #  return None

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

    # Parallelize scraping for better performance
    with concurrent.futures.ThreadPoolExecutor() as executor:
        scraped_data = list(executor.map(scrape, listing_ids))

    write_to_excel(scraped_data, output_excel_file)
    write_to_json(scraped_data, output_json_file)

if __name__ == "__main__":
    main()
