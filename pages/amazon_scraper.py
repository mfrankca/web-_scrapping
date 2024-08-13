import requests
from bs4 import BeautifulSoup

# Function to fetch and parse the Amazon product page
def scrape_amazon_product(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    # Check if request was successful
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract product details
    product_details = {}
    title = soup.find(id='productTitle')
    if title:
        product_details['Title'] = title.get_text(strip=True)

    price = soup.find('span', {'id': 'priceblock_ourprice'}) or soup.find('span', {'id': 'priceblock_dealprice'})
    if price:
        product_details['Price'] = price.get_text(strip=True)

    rating = soup.find('span', {'id': 'acrPopover'})
    if rating:
        product_details['Rating'] = rating.get_text(strip=True)

    return product_details

# Example usage
if __name__ == "__main__":
    url = 'https://www.amazon.com/dp/B08N5WRWNW'  # Replace with the product URL
    details = scrape_amazon_product(url)
    if details:
        for key, value in details.items():
            print(f'{key}: {value}')
