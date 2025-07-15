import pandas as pd
import json

def load_transactions(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

import pandas as pd

def normalize_transactions(data):
    df = pd.json_normalize(data)
    
    if 'userWallet' not in df.columns:
        raise KeyError("❗ 'userWallet' not found in transaction data columns")

    df.rename(columns={'userWallet': 'walletAddress'}, inplace=True)

    # Convert amount to numeric and split deposit/redeem
    df['actionData.amount'] = pd.to_numeric(df['actionData.amount'], errors='coerce')
    df['deposit_amount'] = df.apply(lambda row: row['actionData.amount'] if row['action'] == 'deposit' else 0, axis=1)
    df['redeem_amount'] = df.apply(lambda row: row['actionData.amount'] if row['action'] == 'redeem' else 0, axis=1)

    # Normalize amounts (USDC/USDT are 6 decimals)
    df['actionData.amount'] = pd.to_numeric(df['actionData.amount'], errors='coerce') / 1e6

    
    return df
