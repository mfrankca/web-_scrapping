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

ebay_feedback_site1 = st.secrets["ebay_feedback_site1"]
ebay_feedback_site2 = st.secrets["ebay_feedback_site2"]

st.set_page_config(page_title='Ebay Reviews', page_icon='🎉'  )
st.title('Ebay Reviews')

def clean_item_description(description):
    # Regular expression to find text before '(#'
    cleaned_description = re.sub(r'\s*\(#.*$', '', description)
    return cleaned_description

def save_reviews_to_excel(reviews, file_path):
    df = pd.DataFrame(reviews)
    df.to_excel(file_path, index=False)
    
def get_ebay_reviews(store_url,max_entries=200):
     # Initialize the WebDriver (assuming using ChromeDriver)
    driver = webdriver.Chrome()
    driver.get(store_url)
    

        
    feedbacks = []
    current_page = 0

   
    while len(feedbacks) < max_entries:


        # Wait for items per page button and click to set to 200
        items_per_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="pagination-item-page-4"]'))
        )
        driver.execute_script("arguments[0].click();", items_per_page_button)
        time.sleep(5)  # Wait for the page to reload with 200 items per page

        # Get current page source after setting items per page to 200
        page_source = driver.page_source
        
        # Parse the current page with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        # Locate the feedback table
        feedback_table = soup.find('table', id='feedback-cards')
        
        # Iterate through each feedback entry
        if feedback_table:

            # Iterate through each feedback entry
            for row in feedback_table.find_all('tr', {'data-feedback-id': True}):
                feedback = {}
                seen_feedback_ids = set()  # To track feedback IDs and avoid duplicates
                
                # Extract rating
                rating_tag = row.find('svg', {'data-test-id': lambda x: x and x.startswith('fdbk-rating-')})
                feedback['Rating'] = rating_tag['aria-label'] if rating_tag else 'N/A'
                
                # Extract item description
                item_name_element = row.find('span', {'data-test-id': lambda x: x and x.startswith('fdbk-item-')})
                #item_description = clean_item_description(item_name_element.text.strip()) 
                feedback['item_description'] = clean_item_description(item_name_element.text.strip()) if item_name_element else 'N/A'
                
                #comment_element = row.find('span', {'data-test-id': 'fdbk-comment-1'})
                # Extract comments from buyer
                # Extract comments from buyer
                comment_element = row.find('span', {'data-test-id': lambda x: x and x.startswith('fdbk-comment-')})
                feedback['Comments'] = comment_element.text.strip() if comment_element else 'N/A'
                
                feedback_from_element = row.find('span', {'data-test-id': lambda x: x and x.startswith('fdbk-context-')})
                feedback['From'] = feedback_from_element.text.strip() if feedback_from_element else 'N/A'
                
                #feedback_price_element = row.find('span', {'data-test-id': lambda x: x and x.startswith('fdbk-price-')})
                #feedback['Price'] = feedback_price_element.text.strip() if feedback_price_element  else 'N/A'
                
                feedback_when_element = row.find('span', {'data-test-id': lambda x: x and x.startswith('fdbk-time-')})
                feedback['When'] = feedback_when_element.text.strip() if feedback_when_element  else 'N/A'

                #feedbacks.append(feedback)
            #<td><div><span data-test-id="fdbk-time-1" aria-label="Past month">Past month</span></div><div class="card__links"></div></td>
            #<div class="card__price"><span data-test-id="fdbk-price-1">US $229.00</span></div>
            #<div class="card__from"><span data-test-id="fdbk-context-1" aria-label="Feedback left by buyer.">Buyer: v***d</span><span class="no-wrap">&nbsp;(<span data-test-id="fdbk-rating-score-1">56</span><span class="gspr icst2 starIcon" data-test-id="fdbk-rating-icon-1"></span>)</span></div>
              # Find the "Next" button/link and update the URL
              
                # Extract feedback ID
                feedback_id = row['data-feedback-id']

                # Omit feedbacks with any 'N/A' value and duplicates
                if all(value != 'N/A' for value in feedback.values()) and feedback_id not in seen_feedback_ids:
                    seen_feedback_ids.add(feedback_id)
                    feedbacks.append(feedback)

                # Break if we reach the max_entries limit
                if len(feedbacks) >= max_entries:
                    break
        
        # Simulate clicking the "Next" button if we need more feedback
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'button#next-page')
            if next_button:
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3)  # Wait for the new entries to load

                # Wait until the page content updates
                new_soup = BeautifulSoup(driver.page_source, 'html.parser')
                new_feedback_table = new_soup.find('table', id='feedback-cards')
                if new_feedback_table and new_feedback_table != feedback_table:
                    feedback_table = new_feedback_table
                else:
                    print("Page content did not update, stopping.")
                    break  # If the content did not change, break the loop
            else:
                break  # No more pages
        except Exception as e:
            print("No more pages or an error occurred:", e)
            break  # No more pages or an error occurred
  
    driver.quit()
    return feedbacks

# Example usage
#store_url = "https://www.ebay.com/fdbk/feedback_profile/sunraycity"
#store_url = "https://www.ebay.com/fdbk/feedback_profile/sunraycity?sort=NEWEST"
store_url = "https://www.ebay.com/fdbk/feedback_profile/sunraycity_store?sort=NEWEST"


# Add logo to the sidebar

image_path = "uploads//logo.png"
st.sidebar.image(image_path, use_column_width=True)
st.title("Welcome to SunRayCity Managment")
    
if st.button('Scrape Data'):
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