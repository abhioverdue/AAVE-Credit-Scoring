def compute_score(row):
    score = 0

    # Deposit/Redeem Ratio Weight
    if row['deposit_redeem_ratio'] >= 1:
        score += 300
    elif 0.5 <= row['deposit_redeem_ratio'] < 1:
        score += 150
    else:
        score += 0

    # Transaction Count (10-50 Optimal)
    if 10 <= row['transaction_count'] <= 50:
        score += 300
    elif 5 <= row['transaction_count'] < 10:
        score += 150

    # Unique Assets Weight
    if row['unique_assets'] >= 5:
        score += 250
    elif 3 <= row['unique_assets'] < 5:
        score += 150

    # Average Transaction Size ($500 - $10k ideal)
    if 500 <= row['average_tx_size'] <= 10000:
        score += 150

    return min(score, 1000)
