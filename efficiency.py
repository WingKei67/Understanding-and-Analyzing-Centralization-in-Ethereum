import pandas as pd

# Load the CSV file
df = pd.read_csv("combined_test_files.csv")

# Ensure 'efficiency' column is numeric
df['efficiency'] = pd.to_numeric(df['efficiency'], errors='coerce')

# Drop missing or invalid values
df = df.dropna(subset=['efficiency'])

# Calculate average efficiency
average_efficiency = df['efficiency'].mean()

print(f"Average efficiency: {average_efficiency:.4f}")
