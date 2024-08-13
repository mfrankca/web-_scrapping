import urllib.parse
import urllib.request
import urllib.response
from bs4 import BeautifulSoup

# Function to fetch and parse the Amazon product page
def scrape_amazon_product(url):

    request = urllib.request.urlopen(url)
    
    # Check if request was successful
    response = urllib.request.urlopen(url)
    code = response.getcode()
    if code != 200:
        print("Failed to retrieve the page")
        return None

    soup = BeautifulSoup(request.read(), 'html.parser')

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
    url = 'https://www.amazon.ca/Stylish-Non-prescription-Eyeglasses-Eyeglass-Gradient/dp/B07PY8MQ5M/ref=sr_1_1?crid=3U06ACJEVNQL8&dib=eyJ2IjoiMSJ9.0DPMaxiy5RHMOAe3jYgiNjx2U_l2vejKryfnIhJP_Oe42X7-Ap5be7C2T_71pY-smlLrwMiMkaYU4Ar_4U-1pFMpnwohhSYc44lJCOEjtkPk4zs0eruAY0F65uuVuX_wB6wXFuJwj1Uu0lgjbnmsbxqDCsV94Mpsak6y6j6FL9qPTZ-jO9nlkaqOvZNnvxI16nZcrWAwVyGGq0Vv4jG2sxLA8J6sH2dEAxOPJrky_qxKMjz-wsNpJUo1oN-7ifGgdPD9SeHwfrcwXQA6XpUf1ZsTv5BF1l3rbkzzJr8Ict4.lmcMBgfroCnMyvnQA1bMm6vmzd3t_PEzmPYOxZFUNOk&dib_tag=se&keywords=Fendi+Eyeglasses&qid=1723517219&sprefix=fendi+eyeglasses%2Caps%2C64&sr=8-1'  # Replace with the product URL
    details = scrape_amazon_product(url)
    if details:
        for key, value in details.items():
            print(f'{key}: {value}')
