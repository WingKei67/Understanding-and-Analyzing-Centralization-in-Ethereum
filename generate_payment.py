import pandas as pd

# Load the labeled CSV
df = pd.read_csv("winning_bids_labeled.csv")

# Ensure 'value' is numeric
df['value'] = pd.to_numeric(df['value'], errors='coerce')
df = df.dropna(subset=['builder_label', 'value'])

# Group by builder and calculate total payment value
builder_totals = df.groupby('builder_label')['value'].sum()

# Compute total and individual percentages
total_value = builder_totals.sum()
builder_percent = (builder_totals / total_value) * 100

# Sort builders by individual percentage (descending)
sorted_percent = builder_percent.sort_values(ascending=False)

# Build output with cumulative percentage
cumulative = 0.0
output = []

for builder, percent in sorted_percent.items():
    cumulative += percent
    output.append((builder, percent, cumulative))

# Save to CSV
output_df = pd.DataFrame(output, columns=['builder_label', 'payment_percentage', 'cumulative_percentage'])
output_df.to_csv("cumulative_builder_payment_share.csv", index=False)

print("Saved cumulative builder payment share to 'cumulative_builder_payment_share.csv'")
