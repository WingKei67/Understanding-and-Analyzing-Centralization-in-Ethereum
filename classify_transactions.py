import pandas as pd

# Load CSVs
blocks_df = pd.read_csv("enriched_data/merged_mevboost.csv").drop_duplicates(subset='slot')
txs_df = pd.read_csv("enriched_data/merged_mevboost_txs.csv").drop_duplicates(subset='txhash')
private_txs_df = pd.read_csv("private_transactions.csv")
public_txs_df = pd.read_csv("public_transactions.csv")
print('Finished loading')

# Ensure all txhashes start with "0x"
txs_df['txhash'] = txs_df['txhash'].astype(str).apply(lambda x: x if x.startswith("0x") else "0x" + x)
print('Finished ensuring')

# Ensure types are correct
private_txs_df['hash'] = private_txs_df['hash'].astype(str)
public_txs_df['hash'] = public_txs_df['hash'].astype(str)
txs_df['block_number'] = txs_df['block_number'].astype(int)
blocks_df['block_number'] = blocks_df['block_number'].astype(int)
print('Finished converting')

# Create hash-to-data mappings
private_tx_dict = private_txs_df.set_index('hash')[['gas', 'gas_price', 'gas_tip_cap', 'gas_fee_cap']].to_dict(orient='index')
public_tx_dict = public_txs_df.set_index('hash')[['gas', 'gas_price', 'gas_tip_cap', 'gas_fee_cap']].to_dict(orient='index')
print('Finished mapping')

# Filter blocks by slot range
slot_min = 11163597
slot_max = 11386798
filtered_blocks_df = blocks_df[(blocks_df['slot'] >= slot_min) & (blocks_df['slot'] <= slot_max)].copy()
print('Finished filtering')

# Prepare output files (clear + write headers)
with open("enriched_data/private_transactions_by_block.csv", 'w') as f:
    f.write("slot,block_number,block_hash,builder_pubkey,txhash,gas,gas_price,gas_tip_cap,gas_fee_cap\n")
with open("enriched_data/public_transactions_by_block.csv", 'w') as f:
    f.write("slot,block_number,block_hash,builder_pubkey,txhash,gas,gas_price,gas_tip_cap,gas_fee_cap\n")
with open("enriched_data/block_transaction_summary.csv", 'w') as f:
    f.write("slot,block_hash,builder_pubkey,value,block_number,public_tx_count,private_tx_count,unknown_tx_count\n")

# Function to classify and immediately write transactions
def classify_transactions(block_row):
    block_number = block_row['block_number']
    block_txs = txs_df[txs_df['block_number'] == block_number]
    print(block_number)

    private_count = public_count = unknown_count = 0

    for _, tx in block_txs.iterrows():
        tx_hash = tx['txhash']
        base_record = {
            'slot': block_row['slot'],
            'block_number': block_row['block_number'],
            'block_hash': block_row['block_hash'],
            'builder_pubkey': block_row['builder_pubkey'],
            'txhash': tx_hash
        }

        if tx_hash in private_tx_dict:
            private_count += 1
            row = {**base_record, **private_tx_dict[tx_hash]}
            pd.DataFrame([row]).to_csv("processed/private_transactions_by_block.csv", mode='a', header=False, index=False)
        elif tx_hash in public_tx_dict:
            public_count += 1
            row = {**base_record, **public_tx_dict[tx_hash]}
            pd.DataFrame([row]).to_csv("processed/public_transactions_by_block.csv", mode='a', header=False, index=False)
        else:
            unknown_count += 1
        if int(block_row['tx_count']) < private_count + public_count + unknown_count:
            print('sb')
            exit(1)

    return public_count, private_count, unknown_count

# Process blocks, classify, and write summary row-by-row
for _, block_row in filtered_blocks_df.iterrows():
    public_c, private_c, unknown_c = classify_transactions(block_row)
    summary_row = {
        'slot': block_row['slot'],
        'block_hash': block_row['block_hash'],
        'builder_pubkey': block_row['builder_pubkey'],
        'value': block_row['value'],
        'block_number': block_row['block_number'],
        'public_tx_count': public_c,
        'private_tx_count': private_c,
        'unknown_tx_count': unknown_c
    }
    pd.DataFrame([summary_row]).to_csv("processed/block_transaction_summary.csv", mode='a', header=False, index=False)

print("Saved:")
print("- processed/block_transaction_summary.csv")
print("- processed/private_transactions_by_block.csv")
print("- processed/public_transactions_by_block.csv")
