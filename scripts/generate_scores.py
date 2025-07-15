import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processing import load_transactions, normalize_transactions
from src.feature_engineering import extract_wallet_features
from src.scoring_model import compute_score

def main():
    data = load_transactions('data/raw/user-transactions.json')
    df = normalize_transactions(data)

    features = extract_wallet_features(df)
    if features.empty:
        print("❗ No wallet features extracted. Check your input data.")
        return

    features.to_csv('data/processed/wallet_features.csv', index=False)
    print("✅ Wallet features saved at 'data/processed/wallet_features.csv'")

    features['credit_score'] = features.apply(compute_score, axis=1)

    features.to_csv('data/processed/wallet_scores.csv', index=False)
    print("✅ Scores saved at 'data/processed/wallet_scores.csv'")

if __name__ == "__main__":
    main()

