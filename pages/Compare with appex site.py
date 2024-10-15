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

# Function to compare 'SKU' field of two dataframes
def compare_skus(combined_df, comparison_df):
    # Ensure SKU is a string to avoid mismatches
    combined_df['SKU'] = combined_df['Listing ID'].astype(str)
    comparison_df['SKU'] = comparison_df['SKU'].astype(str)

    # Find SKUs in comparison_df not in combined_df
    missing_in_combined = comparison_df[~comparison_df['SKU'].isin(combined_df['SKU'])]

    # Find SKUs in combined_df not in comparison_df
    missing_in_comparison = combined_df[~combined_df['SKU'].isin(comparison_df['SKU'])]

    return missing_in_combined, missing_in_comparison

# Main Streamlit app function
def main():
    st.title("CSV File Combiner and SKU Comparator")
    
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

        # Compare the 'SKU' fields
        missing_in_combined, missing_in_comparison = compare_skus(combined_df, comparison_df)

        # Display missing records in combined file (exists in comparison but not in combined)
        st.write("Missing in Combined File (exists in Comparison):")
        st.write(missing_in_combined)

        # Display missing records in comparison file (exists in Combined but not in Comparison)
        st.write("Missing in Comparison File (exists in Combined):")
        st.write(missing_in_comparison)

        # Provide option to download the missing records (comparison file missing in combined)
        if not missing_in_combined.empty:
            csv_missing_combined = missing_in_combined.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Missing in Combined",
                data=csv_missing_combined,
                file_name='missing_in_combined.csv',
                mime='text/csv'
            )

        # Provide option to download the missing records (combined file missing in comparison)
        if not missing_in_comparison.empty:
            csv_missing_comparison = missing_in_comparison.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Missing in Comparison",
                data=csv_missing_comparison,
                file_name='missing_in_comparison.csv',
                mime='text/csv'
            )

if __name__ == "__main__":
    main()
