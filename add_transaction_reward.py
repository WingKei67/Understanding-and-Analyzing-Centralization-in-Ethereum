import pandas as pd
import time
from web3 import Web3

# === STEP 1: Load Infura Key and Connect ===
with open("./key/infura3.txt", "r") as f:
    RPC_ENDPOINT = f.read().strip()

w3 = Web3(Web3.HTTPProvider(RPC_ENDPOINT))

# === STEP 2: Load Raw Public & Private Transactions ===
pub_tx = pd.read_csv("public_transactions.csv")[["hash", "gas", "gas_price", "gas_tip_cap", "gas_fee_cap"]].rename(columns={"hash": "txhash"})
priv_tx = pd.read_csv("private_transactions.csv")[["hash", "gas", "gas_price", "gas_tip_cap", "gas_fee_cap"]].rename(columns={"hash": "txhash"})

# === STEP 3: Load Block Numbers from Processed Transaction Blocks ===
pub_block = pd.read_csv("processed/public_transactions_by_block.csv")
priv_block = pd.read_csv("processed/private_transactions_by_block.csv")

all_blocks = pd.concat([
    pub_block["block_number"],
    priv_block["block_number"]
]).dropna().astype(int).unique()

print(f"Fetching base fee for {len(all_blocks)} unique blocks...")

# === STEP 4: Fetch base_fee_per_gas from Web3 ===
records = []
for block_num in sorted(all_blocks):
    try:
        block = w3.eth.get_block(int(block_num))
        records.append({
            "block_number": block.number,
            "base_fee_per_gas": block.baseFeePerGas
        })
        time.sleep(0.2)
    except Exception as e:
        print(f"Error at block {block_num}: {e}")

# === STEP 5: Save base fee file ===
base_fee_df = pd.DataFrame(records)
base_fee_df.to_csv("processed/block_base_fees.csv", index=False)
print("Saved base_fee_per_gas to processed/block_base_fees.csv")

# === STEP 6: Define Builder Reward Function ===
def compute_reward(row):
    gas = row["gas"]
    base_fee = row["base_fee_per_gas"]
    if pd.notnull(row["gas_fee_cap"]):
        priority_fee = min(row["gas_tip_cap"], row["gas_fee_cap"] - base_fee)
    else:
        priority_fee = row["gas_price"] - base_fee
    return gas * max(priority_fee, 0)

# === STEP 7: Enrich and Save Public Transactions ===
pub_enriched = pub_block.merge(pub_tx, on="txhash", how="left")
pub_enriched = pub_enriched.merge(base_fee_df, on="block_number", how="left")
pub_enriched["builder_reward"] = pub_enriched.apply(compute_reward, axis=1)
pub_enriched.to_csv("processed/public_transactions_by_block.csv", index=False)
print("Enriched public_transactions_by_block.csv with builder_reward")

# === STEP 8: Enrich and Save Private Transactions ===
priv_enriched = priv_block.merge(priv_tx, on="txhash", how="left")
priv_enriched = priv_enriched.merge(base_fee_df, on="block_number", how="left")
priv_enriched["builder_reward"] = priv_enriched.apply(compute_reward, axis=1)
priv_enriched.to_csv("processed/private_transactions_by_block.csv", index=False)
print("Enriched private_transactions_by_block.csv with builder_reward")
