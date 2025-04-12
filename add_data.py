import pandas as pd
import glob
import os

# Step 1: Load and concatenate all matching transaction_data CSVs
transaction_files = glob.glob("transaction_data/03-*/2025-03-*.csv")
transaction_data = pd.concat((pd.read_csv(f) for f in transaction_files), ignore_index=True)

# Step 2: Keep only necessary columns and rename txhash to hash for merge
transaction_data = transaction_data[["hash", "gas", "gas_price", "gas_tip_cap", "gas_fee_cap"]]

# Step 3: Load and merge enriched private transactions
private_df = pd.read_csv("processed/private_transactions_by_block.csv")
private_df = private_df.rename(columns={"txhash": "hash"})
private_merged = private_df.merge(transaction_data, on="hash", how="inner")
private_merged.to_csv("processed/private_transactions_enriched.csv", index=False)

# Step 4: Load and merge enriched public transactions
public_df = pd.read_csv("processed/public_transactions_by_block.csv")
public_df = public_df.rename(columns={"txhash": "hash"})
public_merged = public_df.merge(transaction_data, on="hash", how="inner")
public_merged.to_csv("processed/public_transactions_enriched.csv", index=False)
