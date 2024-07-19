import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# Configuration from Streamlit secrets
ebay_feedback_site1 = "https://www.ebay.com/fdbk/feedback_profile/sunraycity?sort=NEWEST"
ebay_feedback_site2 = "https://www.ebay.com/fdbk/feedback_profile/sunraycity_store?sort=NEWEST"
# Set up the Streamlit page
st.set_page_config(page_title='Ebay Reviews', page_icon='🎉')
st.title('Ebay Reviews')

def clean_item_description(description):
    """
    Clean the item description by removing unwanted text patterns.
    
    Args:
        description (str): The item description to be cleaned.
    
    Returns:
        str: The cleaned item description.
    """
    cleaned_description = re.sub(r'\s*\(#.*$', '', description)
    return cleaned_description

def save_reviews_to_excel(reviews, file_path):
    """
    Save the collected reviews to an Excel file.
    
    Args:
        reviews (list of dict): The list of reviews to be saved.
        file_path (str): The file path to save the Excel file.
    """
    df = pd.DataFrame(reviews)
    df.to_excel(file_path, index=False)

def get_ebay_reviews(store_url, max_entries=200):
    """
    Scrape eBay reviews from the given store URL.
    
    Args:
        store_url (str): The URL of the eBay store's feedback page.
        max_entries (int): The maximum number of reviews to scrape.
    
    Returns:
        list of dict: A list of dictionaries containing review data.
    """
    driver = webdriver.Chrome()
    driver.get(store_url)
    
    feedbacks = []
    seen_feedback_ids = set()  # To track feedback IDs and avoid duplicates
    
    while len(feedbacks) < max_entries:
        # Wait for items per page button and click to set to 200
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="pagination-item-page-4"]'))
        ).click()
        time.sleep(5)  # Wait for the page to reload with 200 items per page

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        feedback_table = soup.find('table', id='feedback-cards')

        if feedback_table:
            for row in feedback_table.find_all('tr', {'data-feedback-id': True}):
                feedback = {}
                feedback_id = row['data-feedback-id']
                
                if feedback_id in seen_feedback_ids:
                    continue
                
                seen_feedback_ids.add(feedback_id)
                
                # Extract rating
                rating_tag = row.find('svg', {'data-test-id': lambda x: x and x.startswith('fdbk-rating-')})
                feedback['Rating'] = rating_tag['aria-label'] if rating_tag else 'N/A'
                
                # Extract item description
                item_name_element = row.find('span', {'data-test-id': lambda x: x and x.startswith('fdbk-item-')})
                feedback['item_description'] = clean_item_description(item_name_element.text.strip()) if item_name_element else 'N/A'
                
                # Extract comments from buyer
                comment_element = row.find('span', {'data-test-id': lambda x: x and x.startswith('fdbk-comment-')})
                feedback['Comments'] = comment_element.text.strip() if comment_element else 'N/A'
                
                # Extract feedback from element
                feedback_from_element = row.find('span', {'data-test-id': lambda x: x and x.startswith('fdbk-context-')})
                feedback['From'] = feedback_from_element.text.strip() if feedback_from_element else 'N/A'
                
                # Extract feedback time
                feedback_when_element = row.find('span', {'data-test-id': lambda x: x and x.startswith('fdbk-time-')})
                feedback['When'] = feedback_when_element.text.strip() if feedback_when_element else 'N/A'
                
                # Add feedback to list
                if all(value != 'N/A' for value in feedback.values()):
                    feedbacks.append(feedback)
                
                if len(feedbacks) >= max_entries:
                    break
        
        # Simulate clicking the "Next" button if more feedback is needed
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'button#next-page')
            if next_button:
                next_button.click()
                time.sleep(3)  # Wait for the new entries to load
            else:
                break  # No more pages
        except Exception as e:
            print("No more pages or an error occurred:", e)
            break
    
    driver.quit()
    return feedbacks

def display_sidebar():
    """
    Display the sidebar with a logo image and documentation.
    """
    image_path = "uploads/logo.png"
    st.sidebar.image(image_path, use_column_width=True)
    
    st.sidebar.header('Documentation')
    st.sidebar.write("""
    **Ebay Reviews** is a web application built to manage Eyeware ecommerce store.

    ### Features:
    - **Web Scraping**: Scrape reviews from eBay feedback pages.
    - **Data Export**: Save scraped reviews to an Excel file.

    ### Instructions:
    1. **Choose Site**: Select which eBay feedback site to scrape.
    2. **Enter URL**: Provide the URL of the eBay feedback page.
    3. **Scrape Data**: Click "Scrape Data" to collect and save reviews.

    Supported feedback sites: **eBay Feedback Site 1**, **eBay Feedback Site 2**.
    """)

def main():
    """
    Main function to set up the Streamlit app.
    """
    display_sidebar()

    site_choice = st.selectbox("Choose eBay feedback site", ["ebay_feedback_site1", "ebay_feedback_site2"])
    store_url = ebay_feedback_site1 if site_choice == 'ebay_feedback_site1' else ebay_feedback_site2

    if st.button('Scrape Data'):
        if store_url:
            reviews = get_ebay_reviews(store_url)
            if reviews:
                st.write("Scraping completed!")
                file_path = "reviews.xlsx"
                save_reviews_to_excel(reviews, file_path)
                st.write("Reviews saved to Excel.")
                with open(file_path, "rb") as file:
                    st.download_button(label="Download Excel file", data=file, file_name="reviews.xlsx")
            else:
                st.write("No reviews found or failed to scrape the reviews.")
        else:
            st.write("Please select a valid eBay feedback site.")

if __name__ == "__main__":
    main()
