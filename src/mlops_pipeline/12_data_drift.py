import os
import json
import pandas as pd
from scipy.stats import ks_2samp

def detect_data_drift():
    print("[STAGE 12] Performing Statistical Kolmogorov-Smirnov Data Drift Analysis...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    train_path = os.path.join(base_dir, "data", "processed", "train_dataset.csv")
    evolved_path = os.path.join(base_dir, "data", "monitoring", "drift", "evolved_data.csv")

    df_train = pd.read_csv(train_path)
    df_evolved = pd.read_csv(evolved_path)

    drift_results = {}
    features_drifted = []

    num_cols = df_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if 'price' in num_cols:
        num_cols.remove('price')

    for col in num_cols:
        if col in df_evolved.columns:
            stat, p_val = ks_2samp(df_train[col], df_evolved[col])
            has_drift = bool(p_val < 0.05)
            drift_results[col] = {
                "ks_statistic": round(float(stat), 4),
                "p_value": round(float(p_val), 5),
                "drift_detected": has_drift
            }
            if has_drift:
                features_drifted.append(col)

    print(f"[STAGE 12] Drift Analysis: {len(features_drifted)} feature(s) drifted ({features_drifted}).")
    return drift_results

if __name__ == "__main__":
    detect_data_drift()
