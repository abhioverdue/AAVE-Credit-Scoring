import pandas as pd

def extract_wallet_features(df):
    grouped = df.groupby('walletAddress')

    features = grouped.agg(
        transaction_count=('action', 'count'),
        unique_assets=('actionData.assetSymbol', 'nunique'),
        total_deposit=('deposit_amount', 'sum'),
        total_redeem=('redeem_amount', 'sum'),
        average_tx_size=('actionData.amount', 'mean')
    ).reset_index()

    # Safe deposit/redeem ratio
    features['deposit_redeem_ratio'] = features.apply(
        lambda row: row['total_deposit'] / row['total_redeem']
        if row['total_redeem'] > 0 else row['total_deposit'], axis=1
    )

    # Cap extreme ratios (optional)
    features['deposit_redeem_ratio'] = features['deposit_redeem_ratio'].clip(upper=100)

    return features



