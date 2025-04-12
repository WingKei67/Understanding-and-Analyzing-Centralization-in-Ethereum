import numpy as np
import pandas as pd
import secrets
import time

def simulate_transaction_data(lambda_mean, lambda_std, mu, sigma, duration_sec, tx_type, seed=42):
    np.random.seed(seed)

    # Sample λ (tx/ms), ensure it's positive
    lambda_sim = -1
    while lambda_sim <= 0:
        lambda_sim = np.random.normal(lambda_mean, lambda_std)

    duration_ms = int(duration_sec * 1000)

    # Simulate number of transactions
    num_txs = np.random.poisson(lambda_sim * duration_ms)

    # Inter-arrival times and timestamps (in ms)
    inter_arrival_times = np.random.exponential(scale=1 / lambda_sim, size=num_txs)
    timestamp_ms = np.cumsum(inter_arrival_times)
    timestamp_ms = timestamp_ms[timestamp_ms <= duration_ms].astype(np.int64)

    # Simulated lognormal values (ETH), converted to wei
    values_eth = np.random.lognormal(mean=mu, sigma=sigma, size=len(timestamp_ms))
    values_wei = (values_eth * 1e18).astype(np.int64)

    # Generate random hashes
    hashes = ['0x' + secrets.token_hex(32) for _ in range(len(timestamp_ms))]

    # Normalize time
    start_ms = int(time.time() * 1000)
    timestamp_ms = start_ms + timestamp_ms
    time_elapse = timestamp_ms - timestamp_ms[0]

    # Build DataFrame
    df = pd.DataFrame({
        'timestamp_ms': timestamp_ms,
        'hash': hashes,
        'value': values_wei,
        'tx_type': tx_type,
        'time_elapse': time_elapse
    })

    return df

# Parameters (use your own estimates here)
public_params = {
    'lambda_mean': 0.003822,
    'lambda_std': 0.003547,
    'mu': -6.232609,
    'sigma': 6.512466
}

private_params = {
    'lambda_mean': 0.101790,
    'lambda_std': 0.751070,
    'mu': -12.581832,
    'sigma': 8.972877
}

# 31 days in seconds
duration_days = 31
duration_sec = duration_days * 24 * 60 * 60  # = 2,678,400 seconds

# Simulate
print("Simulating 31 days of public and private transactions...")

public_df = simulate_transaction_data(
    **public_params, duration_sec=duration_sec, tx_type='public', seed=1
)
private_df = simulate_transaction_data(
    **private_params, duration_sec=duration_sec, tx_type='private', seed=2
)

# Save to CSV
public_df.to_csv('simulated_public_transactions.csv', index=False)
private_df.to_csv('simulated_private_transactions.csv', index=False)

print(f"Saved {len(public_df)} public transactions.")
print(f"Saved {len(private_df)} private transactions.")
