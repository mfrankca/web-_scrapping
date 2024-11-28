import streamlit as st
import pandas as pd
from io import BytesIO
def display_sidebar():
    """
    Display the sidebar with a logo image and documentation.
    """
    image_path = "uploads/logo.png"
    st.sidebar.image(image_path, use_column_width=True)
    
    # Documentation section in the sidebar
    with st.sidebar.expander("Documentation", icon="📚"):
        st.write("""
        **SunRayCity Management** is a web application built to manage Eyeware ecommerce store. 
        
        ### Features:
        - **File Upload**: Upload product data in Excel or CSV format.
        - **Data Editing**: Edit the product data directly within the application.
        
        ### Instructions:
        1. **Select File Type**: Choose the file type (Excel or CSV) you want to upload.
        2. **Upload File**: Click on "Upload your file" to upload your product data.
        3. **Edit Data**: Make changes to the data using the provided editor.
        
        Supported file formats: **Excel**, **CSV**.
        """)

def load_colors(file=None):
    # AWS S3 configuration
    BUCKET_NAME = 'sunraycolors'
    EXCEL_FILE_KEY = 'colors.xlsx'
    
    # Initialize S3 client
    s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_default_region
)
  
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=EXCEL_FILE_KEY)
    df = pd.read_excel(BytesIO(response['Body'].read()))
    return df

# Function to get Pantone color information
def get_pantone_color(pantone_number):
    response = requests.get(f"https://connect.pantone.com//id?hex={pantone_number.lstrip('#')}")
    if response.status_code == 200:
        return response.json()
    else:
       st.error("Error fetching Pantone color information.")
       return None

# Function to save DataFrame to S3
def save_to_s3(df, bucket_name, file_name, file_type):
    buffer = BytesIO()
    if file_type == 'xlsx':
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
    elif file_type == 'json':
        df.to_json(buffer, orient='records', indent=2)
    
    buffer.seek(0)
    # Initialize S3 client
    s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_default_region
)
    s3_client.upload_fileobj(buffer, bucket_name, file_name)
    
# Function to load DataFrame    
def load_dataframe(uploaded_file):
    if uploaded_file.name.endswith('.json'):
        df = pd.read_json(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file format")
    return df

def main():
    """
    Main function to set up the Streamlit app.
    """
    display_sidebar()
    
    st.title("Welcome to SunRayCity Management")
    st.header('Color Managemenet')
    
    # AWS S3 configuration
    BUCKET_NAME = 'sunraycolors'
    EXCEL_FILE_KEY = 'colors.xlsx'

    df = load_colors( EXCEL_FILE_KEY)
    if df is not None:
            edited_df=st.data_editor(
    df, num_rows="dynamic", hide_index =False, use_container_width=True)
            
            if st.button('Save Changes'):
                    with pd.ExcelWriter('updated_colors.xlsx', engine='openpyxl') as writer:
                        edited_df.to_excel(writer, index=False)
                        save_to_s3(edited_df, BUCKET_NAME, EXCEL_FILE_KEY, 'xlsx')
                    st.success('Changes saved successfully!')
                    
            # Select a row using a selectbox
            row_options = edited_df.index.tolist()
            selected_row_index = st.selectbox("Select a row to preview color", row_options)
    
            # Get the selected row index
            if selected_row_index is not None:
                    selected_row = edited_df.loc[selected_row_index]
                    color_value = selected_row['RGB Values']
                    color_name = selected_row['Color Name']
                    color_Pantone = selected_row['Pantone Number']
                    # Ensure the color value is valid
                    try:
                        rgb_values = [int(x) for x in color_value.strip('()').split(',')]
                        if len(rgb_values) == 3 and all(0 <= x <= 255 for x in rgb_values):
                            color_hex = '#%02x%02x%02x' % tuple(rgb_values)
                            st.write(f'Selected Color (Color Name): {color_name}')
                            st.write(f'Selected Color (Pantone): { color_Pantone}')
                            st.write(f'Selected Color (RGB): {color_value}')
                            st.write(f'Selected Color (Hex): {color_hex}')
                            st.markdown(
                                f'<div style="width:500px; height:500px; background-color:{color_hex};"></div>',
                                unsafe_allow_html=True
                            )

                        else:
                            st.error("Invalid RGB color value. Ensure it is in the format (R, G, B) with values between 0 and 255.")
                    except:
                        st.error("Invalid RGB color value. Ensure it is in the format (R, G, B) with values between 0 and 255.")
            else:
                    st.write('Select a row to see the color preview.')  

if __name__ == "__main__":
    main()