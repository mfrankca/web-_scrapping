import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import sys
# Define the eBay listing URL
listing_url = "https://www.ebay.com/itm/295901481614"

# Download the HTML content of the listing page
response = requests.get(listing_url)
soup = BeautifulSoup(response.content, "html.parser")

# Extract relevant details
listing_id = soup.find("div", {"iid": True})["iid"]
listing_title = soup.find("h1", {"class": "it-ttl"}).text.strip()
listing_price = soup.find("span", {"id": "prcIsum"}).text.strip()

# Print the scraped details
print(f"Listing ID: {listing_id}")
print(f"Title: {listing_title}")
print(f"Price: {listing_price}")