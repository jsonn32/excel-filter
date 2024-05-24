import pandas as pd

def compare_csv_files(file1, file2):
    # Load the CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Check if the shape (number of rows and columns) is the same
    if df1.shape != df2.shape:
        print("The files have different shapes.")
        return False

    # Check for differences
    comparison_result = df1.equals(df2)

    if comparison_result:
        print("The files are identical.")
    else:
        print("The files are different.")
        # Optionally, display the differences
        diff = df1.compare(df2)
        print(diff)
    
    return comparison_result

# File paths for the two CSV files to compare
file1 = 'final_cleaned_addresses.csv'
file2 = 'correct.csv'

# Compare the files
are_files_identical = compare_csv_files(file1, file2)
