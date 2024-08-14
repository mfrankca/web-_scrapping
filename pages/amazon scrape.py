from bs4 import BeautifulSoup
import requests
import streamlit as st

# Connect to Website and pull in data
URL = 'https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3&customId=B0752XJYNL&th=1'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

page = requests.get(URL)
soup1 = BeautifulSoup(page.content, "html.parser")

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
