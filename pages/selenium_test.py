import streamlit as st
import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

username = "reddiveusa@gmail.com" 
password = "Profit44" 

# Initialize Selenium WebDriver

def get_website_content(url):
    driver = None
    try:
        # Using on Local
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
        st.write(f"DEBUG:DRIVER:{driver}")
        st.write(url)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        feedback_table = soup.find('table', id='feedback-cards')

        #driver.quit()
    
        return feedback_table
    except Exception as e:
        st.write(f"DEBUG:INIT_DRIVER:ERROR:{e}")
    finally:
        if driver is not None: driver.quit()
    return None

# ---------------- Page & UI/UX Components ------------------------
def main_sidebar():
    # 1.Vertical Menu
    st.header("Running Selenium on Streamlit Cloud")
    site_extraction_page()


def site_extraction_page():
    SAMPLE_URL = 'https://www.ebay.com/fdbk/feedback_profile/sunraycity?sort=NEWEST'
    url = st.text_input(label="URL", placeholder='https://www.ebay.com/fdbk/feedback_profile/sunraycity?sort=NEWEST', value=SAMPLE_URL)

    clicked = st.button("Load Page Content",type="primary")
    if clicked:
        with st.container(border=True):
            with st.spinner("Loading page website..."):
                content = get_website_content(url)
                st.write(content)


if __name__ == "__main__":
    main_sidebar()
  

"""   
url = 'https://www.ebay.com/itm/294453072910'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

title_element = soup.find('h1', attrs={'class': 'x-item-title__mainTitle'})
title=title_element.text.replace('Details about', '').strip() if title_element else 'Not Available'
st.write(title)
"""