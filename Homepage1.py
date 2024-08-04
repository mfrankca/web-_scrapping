import streamlit as st

def display_sidebar():
    """
    Display the sidebar with a logo image and documentation.
    """
    image_path = "uploads/logo.png"
    st.sidebar.image(image_path, use_column_width=True)
    
    with st.sidebar.expander("Documentation", icon="📚"):
        st.write("""
        **Welcome to the SunRayCity Management Tool**

        ### About SunRayCity Sunglasses
        At SunRayCity Sunglasses, we search the world for the best deals on fashion and sport sunglasses. We only sell authentic and brand name sunglasses. If you are searching for a specific model that you cannot find on the site, send us an email at [sales@sunraycity.com](mailto:sales@sunraycity.com) and we will do our best to find it. We operate online only to offer these deals.

        ### Features
        - **Manage Customers**: Keep track of customer details and interactions.
        - **Product Catalog Management**: Maintain and update the product catalog.
        - **eBay Product Catalog Scraping**: Scrape product data from eBay.
        - **Scrape eBay Reviews**: Scrape reviews from the following eBay feedback pages:
          - [SunRayCity eBay Store 1](https://www.ebay.com/fdbk/feedback_profile/sunraycity)
          - [SunRayCity eBay Store 2](https://www.ebay.com/fdbk/feedback_profile/sunraycity_store)
        - **Compare Product Catalogs**: Compare the product catalog on eBay vs. the SunRayCity website.
""")
def main():        
    st.set_page_config(
        page_title="Ex-stream-ly Cool App",
        page_icon="c:\Moshe Sunglasses\Pictures\logo\favicon.ico",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )
    st.markdown("<h1 style='text-align: center; color: grey;'>Welcome to SunRayCity Management Tool</h1>", unsafe_allow_html=True)

    st.header(":blue[cool] :sunglasses:",divider='rainbow')  
    #image_path = "uploads//logo.png"
    image_path = "uploads//sunglasses.png"
    st.image(image_path, use_column_width=True)
    display_sidebar()
    
 
if __name__ == "__main__":
    main() 