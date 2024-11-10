import pandas as pd

# File paths
input_file = 'stock_data_history.csv'
output_file = 'filtered_stock_data.csv'

try:
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Filter out rows where the 'Quantity' column is 0
    filtered_df = df[df['Quantity'] != 0]

    # Write the filtered data to the output file
    filtered_df.to_csv(output_file, index=False)

    print(f"Filtered data successfully written to '{output_file}'.")

except FileNotFoundError:
    print(f"Error: The file '{input_file}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
