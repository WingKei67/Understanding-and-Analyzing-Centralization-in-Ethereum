import pandas as pd

# File paths
public_file = 'public_transactions.csv'
private_file = 'private_transactions.csv'

# Read CSV files
public_df = pd.read_csv(public_file)
private_df = pd.read_csv(private_file)

# Count rows
public_count = len(public_df)
private_count = len(private_df)
total_count = public_count + private_count

# Output results
print(f"Number of rows in public_transactions.csv: {public_count}")
print(f"Number of rows in private_transactions.csv: {private_count}")
print(f"Total number of transactions: {total_count}")
