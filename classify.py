import os
import pandas as pd
from glob import glob

# Path to all transaction folders
base_dir = 'transaction_data'
month_pattern = os.path.join(base_dir, '03-*')
all_days = sorted(glob(month_pattern))

public_txs = []
private_txs = []

for day_dir in all_days:
    tx_file = glob(os.path.join(day_dir, '2025-03-??.csv'))
    sourcelog_file = glob(os.path.join(day_dir, '2025-03-*_sourcelog.csv'))

    # Include 'included_at_block_height' and ensure necessary filtering
    tx_df = pd.read_csv(tx_file[0], usecols=['timestamp_ms', 'hash', 'gas' ,'gas_price', 'gas_tip_cap', 'gas_fee_cap', 'included_at_block_height'])
    tx_df = tx_df[tx_df['included_at_block_height'] != 0].drop_duplicates(subset='hash')

    sourcelog_df = pd.read_csv(sourcelog_file[0], usecols=['hash'])

    # Count how many times each hash appears in the sourcelog
    hash_counts = sourcelog_df['hash'].value_counts()

    # Tag as private (only 1 appearance) or public (>1)
    tx_df['tx_type'] = tx_df['hash'].map(lambda h: 'public' if hash_counts.get(h, 0) > 1 else 'private')

    # Split and store
    public_txs.append(tx_df[tx_df['tx_type'] == 'public'])
    private_txs.append(tx_df[tx_df['tx_type'] == 'private'])

# Combine all and sort by included_at_block_height then timestamp_ms
public_all = pd.concat(public_txs).sort_values(by=['included_at_block_height', 'timestamp_ms']).reset_index(drop=True)
private_all = pd.concat(private_txs).sort_values(by=['included_at_block_height', 'timestamp_ms']).reset_index(drop=True)

# Save to CSV
public_all = public_all[public_all['included_at_block_height'] != 0].drop_duplicates(subset='hash')
private_all = private_all[private_all['included_at_block_height'] != 0].drop_duplicates(subset='hash')

public_all.to_csv('public_transactions.csv', index=False)
private_all.to_csv('private_transactions.csv', index=False)

print("Aggregation complete.")
print("public_transactions.csv created.")
print("private_transactions.csv created.")
