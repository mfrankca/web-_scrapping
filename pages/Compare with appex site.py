import streamlit as st
import pandas as pd

# Function to combine uploaded files into a single dataframe
def combine_csv_files(uploaded_files):
    combined_df = pd.DataFrame()  # Initialize an empty dataframe
    for file in uploaded_files:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
            combined_df = pd.concat([combined_df, df], ignore_index=True)
    return combined_df

# Function to compare 'description' field of two dataframes
def compare_descriptions(combined_df, comparison_df):
    # Take only the first 20 characters of the 'description' field for comparison
    combined_df['short_description'] = combined_df['Listing ID']
    comparison_df['short_description'] = comparison_df['SKU']

    # Find records in comparison_df that are not in combined_df based on short_description
    missing_records = comparison_df[~comparison_df['short_description'].isin(combined_df['short_description'])]
    return missing_records

# Main Streamlit app function
def main():
    st.title("CSV File Combiner and Comparator")
    
    # Upload multiple CSV files to combine
    uploaded_files = st.file_uploader("Upload CSV files to combine", accept_multiple_files=True, type=['csv'])
    
    # Upload a CSV file for comparison
    comparison_file = st.file_uploader("Upload CSV file for comparison", type=['csv'])

    if uploaded_files and comparison_file:
        # Combine the uploaded CSV files
        combined_df = combine_csv_files(uploaded_files)

        # Display combined dataframe
        st.write("Combined CSV Data:")
        st.write(combined_df)

        # Read the comparison file
        comparison_df = pd.read_csv(comparison_file)

        # Compare the 'description' fields
        missing_records = compare_descriptions(combined_df, comparison_df)

        # Display missing records
        st.write("Missing Records in Combined File:")
        st.write(missing_records)

        # Provide option to download the missing records as a CSV
        if not missing_records.empty:
            csv = missing_records.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Missing Records",
                data=csv,
                file_name='missing_records.csv',
                mime='text/csv'
            )

if __name__ == "__main__":
    main()
