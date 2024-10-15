import streamlit as st
import pandas as pd

# Function to combine uploaded files into a single dataframe
def combine_csv_files(uploaded_files):
    combined_df = pd.DataFrame()  # Initialize an empty dataframe
    for file in uploaded_files:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
            combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    # Remove rows where 'Listing ID' is null or empty
    #combined_df = combined_df.dropna(subset=['Listing ID'])  # Drop null Listing IDs
    #combined_df = combined_df[combined_df['Listing ID'].str.strip() != '']  # Remove empty Listing ID rows
    return combined_df

# Function to compare 'Listing ID' in combined_df with 'SKU' in comparison_df
def compare_listing_ids_to_skus(combined_df, comparison_df):
    # Ensure Listing ID and SKU are strings to avoid mismatches
    combined_df['SKU'] = combined_df['Listing ID'].astype(str)
    comparison_df['SKU'] = comparison_df['SKU'].astype(str)

    # Remove rows where 'SKU' is null or empty in comparison dataframe
    comparison_df = comparison_df.dropna(subset=['SKU'])  # Drop null SKUs in comparison file
    comparison_df = comparison_df[comparison_df['SKU'].str.strip() != '']  # Remove empty SKU rows

    # Find SKUs in comparison_df not in combined_df (based on Listing ID)
    missing_in_combined = comparison_df[~comparison_df['SKU'].isin(combined_df['SKU'])]

    # Find Listing IDs in combined_df not in comparison_df (based on SKU)
    missing_in_comparison = combined_df[~combined_df['SKU'].isin(comparison_df['SKU'])]

    return missing_in_combined, missing_in_comparison

# Main Streamlit app function
def main():
    st.title("CSV File Combiner and Listing ID to SKU Comparator")
    
    # Upload multiple CSV files to combine
    uploaded_files = st.file_uploader("Upload CSV files to combine", accept_multiple_files=True, type=['csv'])
    
    # Upload a CSV file for comparison
    comparison_file = st.file_uploader("Upload CSV file for comparison", type=['csv'])

    if uploaded_files and comparison_file:
        # Combine the uploaded CSV files
        combined_df = combine_csv_files(uploaded_files)

        # Display combined dataframe
        st.write("Combined CSV Data (valid Listing IDs only):")
        st.write(combined_df)

        # Read the comparison file
        comparison_df = pd.read_csv(comparison_file)

        # Compare 'Listing ID' from combined files with 'SKU' from comparison file
        missing_in_combined, missing_in_comparison = compare_listing_ids_to_skus(combined_df, comparison_df)

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