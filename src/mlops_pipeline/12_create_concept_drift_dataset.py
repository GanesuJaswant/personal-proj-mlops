import os
import pandas as pd
import numpy as np

def create_concept_drift_dataset():
    print("[STAGE 12] Generating Concept Drift Dataset (Market Dynamic Shift)...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_raw_path = os.path.join(base_dir, "data", "raw", "CarPrice_Assignment.csv")
    drift_dir = os.path.join(base_dir, "data", "monitoring", "drift")
    os.makedirs(drift_dir, exist_ok=True)

    if not os.path.exists(data_raw_path):
        data_raw_path = os.path.join(base_dir, "data", "raw", "churn.csv")

    df = pd.read_csv(data_raw_path)
    drifted = df.copy()

    # Shift relationship: fuel efficiency valued much higher due to fuel price shocks
    if 'citympg' in drifted.columns and 'price' in drifted.columns:
        drifted['price'] = (drifted['price'] + (drifted['citympg'] * 350.0)).round(2)

    save_path = os.path.join(drift_dir, "evolved_labeled_data.csv")
    drifted.to_csv(save_path, index=False)
    print(f"[STAGE 12] Concept drift dataset updated at: {save_path}")
    return True

if __name__ == "__main__":
    create_concept_drift_dataset()
