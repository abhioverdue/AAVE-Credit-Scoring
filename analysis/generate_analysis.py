import pandas as pd

# Load data
df = pd.read_csv('data/processed/wallet_scores.csv')

# Define score ranges
bins = [0, 100, 200, 400, 600, 800, 1000]
labels = ['0-100', '100-200', '200-400', '400-600', '600-800', '800-1000']
df['score_range'] = pd.cut(df['credit_score'], bins=bins, labels=labels, right=False)

# Score distribution
score_dist = df['score_range'].value_counts().sort_index().reset_index()
score_dist.columns = ['Score Range', 'Wallet Count']
score_dist['Percentage'] = (score_dist['Wallet Count'] / len(df) * 100).round(1)

print("=== Score Distribution Summary ===")
print(score_dist.to_string(index=False))

# Behavior summary
summary = df.groupby('score_range').agg({
    'transaction_count': 'mean',
    'deposit_redeem_ratio': 'mean',
    'unique_assets': 'mean',
    'average_tx_size': 'mean'
}).rename(columns={
    'transaction_count': 'Avg Transactions/Month',
    'deposit_redeem_ratio': 'Avg Deposit/Redeem Ratio',
    'unique_assets': 'Avg Unique Assets',
    'average_tx_size': 'Avg Transaction Size ($)'
}).reset_index()

print("\n=== Behavior Summary by Score Range ===")
print(summary.to_string(index=False))

# High-risk behavior flags (only if any wallets in 0–100)
high_risk_wallets = df[df['score_range'] == '0-100']

if not high_risk_wallets.empty:
    flag1 = (high_risk_wallets['deposit_redeem_ratio'] < 0.5).sum()
    flag2 = (high_risk_wallets['unique_assets'] <= 2).sum()

    print(f"\n⚠️  High-risk wallets with deposit/redeem ratio < 0.5: {(flag1 / len(high_risk_wallets) * 100):.1f}%")
    print(f"⚠️  High-risk wallets using <= 2 assets: {(flag2 / len(high_risk_wallets) * 100):.1f}%")
else:
    print("\nℹ️  No wallets found in high-risk (0–100) segment to analyze.")

