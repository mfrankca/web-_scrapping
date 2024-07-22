import streamlit as st

def display_sidebar():
    """
    Display the sidebar with a logo image and documentation.
    """
    image_path = "uploads/logo.png"
    st.sidebar.image(image_path, use_column_width=True)
    
    with st.sidebar.expander("Documentation", icon="📚"):
        st.write("""
        **Ebay Reviews** is a web application built to manage eBay reviews.

        ### Features:
        - **Web Scraping**: Scrape reviews from eBay feedback pages.
        - **Data Export**: Save scraped reviews to an Excel file.

        ### Instructions:
        1. **Choose Site**: Select which eBay feedback site to scrape.
        2. **Scrape Data**: Click "Scrape Data" to collect and save reviews.

        Supported feedback sites: **eBay Feedback Site 1**, **eBay Feedback Site 2**.
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
    #image_path = "uploads/logo.png"
    #st.sidebar.image(image_path, use_column_width=True)
    #with st.sidebar.beta_expander("See Documentation",  icon="📚"):
    #    st.write("""
    #   **SunRayCity Management** is a web application built to manage Eyeware ecommerce store. 
        
        ### Features:
    #   - **File Upload**: Upload product data in Excel or CSV format.
    #   - **Data Editing**: Edit the product data directly within the application.
        
        ### Instructions:
    #    1. **Select File Type**: Choose the file type (Excel or CSV) you want to upload.
    #    2. **Upload File**: Click on "Upload your file" to upload your product data.
    #   3. **Edit Data**: Make changes to the data using the provided editor.
    #   
    #   Supported file formats: **Excel**, **CSV**.
    #   """)
 
if __name__ == "__main__":
    main() 