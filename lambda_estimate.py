import pandas as pd

# Load the data
df = pd.read_csv("processed/block_transaction_summary2.csv")

# Compute lambda for public and private transactions
df["lambda_public"] = df["public_tx_count"] / 1200
df["lambda_private"] = df["private_tx_count"] / 1200
df["lambda_unknown_tx_count"] = df["unknown_tx_count"] / 1200


# Calculate mean and standard deviation
mean_lambda_public = df["lambda_public"].mean()
std_lambda_public = df["lambda_public"].std()

mean_lambda_private = (df["lambda_private"] + df["lambda_unknown_tx_count"]).mean()
std_lambda_private = (df["lambda_private"] + df["lambda_unknown_tx_count"]).std()

# Print results
print(f"Public Transaction Count: {df['public_tx_count'].mean():.4f}")
print(f"Private Transaction Count: {(df['private_tx_count'] + df['unknown_tx_count']).mean():.4f}")
print(f"Public Transactions λ (mean): {mean_lambda_public:.4f}, std: {std_lambda_public:.4f}")
print(f"Private Transactions λ (mean): {mean_lambda_private:.4f}, std: {std_lambda_private:.4f}")
