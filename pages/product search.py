import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def login_to_ebay(driver, username, password):
    driver.get("https://www.ebay.com/signin/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "userid"))).send_keys(username)
    driver.find_element(By.ID, "signin-continue-btn").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pass"))).send_keys(password)
    driver.find_element(By.ID, "sgnBt").click()

def get_cookies(driver):
    return driver.get_cookies()

def scrape_ebay_sold_items(username, password):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    login_to_ebay(driver, username, password)
    time.sleep(5)  # Wait for the login process to complete

    # Navigate to the research tab
    research_url = 'https://www.ebay.com/sh/research?marketplace=EBAY-US&keywords=Bolle+Parole+%2F+Vigilante+Sunglasses+Temple+Tips+Matte+Black+Set+x+2&dayRange=90&endDate=1722810843753&startDate=1715034843753&categoryId=0&offset=0&limit=50&tabName=SOLD&tz=America%2FToronto'
    driver.get(research_url)
    time.sleep(5)  # Wait for the page to load

    # Get cookies from the driver and set them in requests session
    session = requests.Session()
    for cookie in get_cookies(driver):
        session.cookies.set(cookie['name'], cookie['value'])

    driver.quit()

    # Now use requests and BeautifulSoup to scrape the data
    items = []
    while True:
        response = session.get(research_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        item_elements = soup.select('div.s-item__info')

        if not item_elements:
            break  # Exit if no items found (end of pagination)

        for item in item_elements:
            description_element = item.select_one('h3.s-item__title')
            price_element = item.select_one('span.s-item__price')
            if description_element and price_element:
                items.append({
                    'Description': description_element.get_text(strip=True),
                    'Price': price_element.get_text(strip=True)
                })

        # Check for next page link
        next_page_link = soup.select_one('a.pagination__next')
        if next_page_link:
            research_url = next_page_link['href']
            time.sleep(3)  # Wait before making the next request
        else:
            break

    # Save the scraped data to an Excel file
    df = pd.DataFrame(items)
    df.to_excel('sold_items.xlsx', index=False)

if __name__ == "__main__":
    username = 'reddiveusa@gmail.com'
    password = 'Profit44'
    scrape_ebay_sold_items(username, password)