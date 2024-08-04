import streamlit as st
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

searchterm = 'shure+sm7b'

def get_data(searchterm):
    url = f'https://www.ebay.com/sh/research?marketplace=EBAY-US&keywords=Bolle+Parole+%2F+Vigilante+Sunglasses+Temple+Tips+Matte+Black+Set+x+2&dayRange=90&endDate=1722810843753&startDate=1715034843753&categoryId=0&offset=0&limit=50&tabName=SOLD&tz=America%2FToronto'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    for item in results:
        product = {
            'title': item.find('h3', {'class': 's-item__title s-item__title--has-tags'}).text,
            'soldprice': float(item.find('span', {'class': 's-item__price'}).text.replace('£','').replace(',','').strip()),
            'solddate': item.find('span', {'class': 's-item__title--tagblock__COMPLETED'}).find('span', {'class':'POSITIVE'}).text,
            'bids': item.find('span', {'class': 's-item__bids'}).text,
            'link': item.find('a', {'class': 's-item__link'})['href'],
        }
        productslist.append(product)
    return productslist

def output(productslist, searchterm):
    productsdf =  pd.DataFrame(productslist)
    productsdf.to_csv(searchterm + 'output.csv', index=False)
    st.write('Saved to CSV')
    return

soup = get_data(searchterm)
productslist = parse(soup)
output(productslist, searchterm)