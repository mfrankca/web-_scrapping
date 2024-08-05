import requests
from bs4 import BeautifulSoup
import streamlit as st

url = "https://www.ebay.com/sh/research?marketplace=EBAY-US&tabName=SOLD"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    st.write(soup.prettify())
    products = []

    for item in soup.find_all('div', class_='sold-result-table'):  # Update with the actual class name
        product_name = item.find('h3', class_='product-title').text.strip()
        product_price = item.find('span', class_='product-price').text.strip()
        products.append({
            'name': product_name,
            'price': product_price
        })

    for product in products:
        st.write(f"Product Name: {product['name']}, Price: {product['price']}")
else:
    st.write("Failed to retrieve the page")