import streamlit as st
import pandas as pd
import re
import asyncio
import nest_asyncio
import threading
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Apply nest_asyncio to allow nesting of event loops
nest_asyncio.apply()

# Configuration from Streamlit secrets
ebay_feedback_site1 = "https://www.ebay.com/fdbk/feedback_profile/sunraycity?sort=NEWEST"
ebay_feedback_site2 = "https://www.ebay.com/fdbk/feedback_profile/sunraycity_store?sort=NEWEST"

# Set up the Streamlit page
st.set_page_config(page_title='Ebay Reviews', page_icon='🎉')
st.title('Ebay Reviews')

def clean_item_description(description):
    cleaned_description = re.sub(r'\s*\(#.*$', '', description)
    return cleaned_description

def save_reviews_to_excel(reviews, file_path):
    df = pd.DataFrame(reviews)
    df.to_excel(file_path, index=False)

def get_ebay_reviews(store_url, max_entries=200):
    reviews = []
    seen_feedback_ids = set()  # To track feedback IDs and avoid duplicates

    def fetch_reviews():
        nonlocal reviews
        nonlocal seen_feedback_ids

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(store_url)

            while len(reviews) < max_entries:
                page.wait_for_selector('table#feedback-cards')

                feedback_table = page.query_selector('table#feedback-cards')
                if not feedback_table:
                    break

                content = page.content()
                soup = BeautifulSoup(content, 'html.parser')
                feedback_table = soup.find('table', id='feedback-cards')

                if feedback_table:
                    for row in feedback_table.find_all('tr', {'data-feedback-id': True}):
                        feedback = {}
                        feedback_id = row['data-feedback-id']
                        
                        if feedback_id in seen_feedback_ids:
                            continue
                        
                        seen_feedback_ids.add(feedback_id)
                        
                        rating_tag = row.find('svg', {'data-test-id': lambda x: x and x.startswith('fdbk-rating-')})
                        feedback['Rating'] = rating_tag['aria-label'] if rating_tag else 'N/A'
                        
                        item_name_element = row.find('span', {'data-test-id': lambda x: x and x.startswith('fdbk-item-')})
                        feedback['item_description'] = clean_item_description(item_name_element.text.strip()) if item_name_element else 'N/A'
                        
                        comment_element = row.find('span', {'data-test-id': lambda x: x and x.startswith('fdbk-comment-')})
                        feedback['Comments'] = comment_element.text.strip() if comment_element else 'N/A'
                        
                        feedback_from_element = row.find('span', {'data-test-id': lambda x: x and x.startswith('fdbk-context-')})
                        feedback['From'] = feedback_from_element.text.strip() if feedback_from_element else 'N/A'
                        
                        feedback_when_element = row.find('span', {'data-test-id': lambda x: x and x.startswith('fdbk-time-')})
                        feedback['When'] = feedback_when_element.text.strip() if feedback_when_element else 'N/A'
                        
                        if all(value != 'N/A' for value in feedback.values()):
                            reviews.append(feedback)
                        
                        if len(reviews) >= max_entries:
                            break
                
                next_button = page.query_selector('button#next-page')
                if next_button:
                    next_button.click()
                    asyncio.sleep(3)
                else:
                    break

            browser.close()

    review_thread = threading.Thread(target=fetch_reviews)
    review_thread.start()
    review_thread.join()
    
    return reviews

def display_sidebar():
    image_path = "uploads/logo.png"
    st.sidebar.image(image_path, use_column_width=True)

    with st.sidebar.expander("Documentation", icon="📚"):
        st.write("""
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