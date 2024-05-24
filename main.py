import pandas as pd

# Define a function to standardize column names
def standardize_columns(df, column_mapping):
    df = df.rename(columns=column_mapping)
    return df

# Define the column mapping for different possible column names
column_mapping = {
    'PropertyID': ['PropertyID', 'PropID', 'ID'],
    'SaleDate': ['SaleDate', 'DateOfSale', 'TransactionDate'],
    'SalePrice': ['SalePrice', 'Price', 'Amount']
}

def process_data(file_path, column_mapping):
    # Load the combined data
    data = pd.read_csv(file_path)

    # Standardize column names
    standardized_columns = {}
    for standard_name, possible_names in column_mapping.items():
        for name in possible_names:
            if name in data.columns:
                standardized_columns[name] = standard_name
                break

    data = standardize_columns(data, standardized_columns)

    # Convert 'SaleDate' to datetime
    data['SaleDate'] = pd.to_datetime(data['SaleDate'])

    # Fill empty 'SalePrice' values with zero and convert to integer
    data['SalePrice'] = data['SalePrice'].fillna(0).astype(int)

    # Sort by 'PropertyID', 'SaleDate', and 'SalePrice' in descending order
    data.sort_values(by=['PropertyID', 'SaleDate', 'SalePrice'], ascending=[True, True, False], inplace=True)

    # Remove duplicates, keeping the first occurrence with the highest SalePrice for each 'PropertyID' and 'SaleDate'
    data = data.drop_duplicates(subset=['PropertyID', 'SaleDate'], keep='first')

    # Sort by 'PropertyID' and 'SaleDate' in descending order
    data.sort_values(by=['PropertyID', 'SaleDate'], ascending=[True, False], inplace=True)

    # Remove duplicates, keeping the first occurrence (most recent sale date) for each 'PropertyID'
    cleaned_data = data.drop_duplicates(subset='PropertyID', keep='first')

    # Remove the time part from 'SaleDate' and split the date into separate columns
    cleaned_data['Sale Date'] = cleaned_data['SaleDate'].dt.strftime('%m/%d/%Y')
    cleaned_data['Sale Month'] = cleaned_data['SaleDate'].dt.month
    cleaned_data['Sale Day'] = cleaned_data['SaleDate'].dt.day
    cleaned_data['Sale Year'] = cleaned_data['SaleDate'].dt.year

    # Reorder columns
    cleaned_data = cleaned_data[['PropertyID', 'Sale Date', 'Sale Month', 'Sale Day', 'Sale Year', 'SalePrice']]

    # Export the final cleaned data to a new CSV file
    final_output_csv_file_path = 'final_cleaned_addresses.csv'
    cleaned_data.to_csv(final_output_csv_file_path, index=False)

    print("DONE")

# Example usage
file_path = 'scraped_addresses.csv'  # Path to the combined CSV file
process_data(file_path, column_mapping)
