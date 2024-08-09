import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By  # Import the By class

try:
    # Setting up Selenium WebDriver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    webdriver.Chrome(service=Service(ChromeDriverManager(version="114.0.5735.90").install()),
                                    options=options)
    # Get the New York Times page
    driver.get("https://nytimes.com")

    # Extract page title
    page_title = driver.title

    # Extract some content from the page (e.g., headline)
    headlines = driver.find_elements(By.TAG_NAME, 'h2')  # Use By.TAG_NAME for finding elements by tag name

    # Display content in Streamlit
    st.title("New York Times - Top Headlines")

    # Display the page title
    st.write(f"Page Title: {page_title}")

    # Loop through the headlines and display them
    for headline in headlines:
        st.write(headline.text)

    # Quit the driver
    driver.quit()

except Exception as e:
        st.write(f"DEBUG:INIT_DRIVER:ERROR:{e}")