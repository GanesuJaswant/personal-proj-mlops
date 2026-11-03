import os
import pandas as pd
import numpy as np

def create_evolved_dataset():
    print("[STAGE 12] Generating Evolved Feature Distribution Dataset...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_raw_path = os.path.join(base_dir, "data", "raw", "CarPrice_Assignment.csv")
    drift_dir = os.path.join(base_dir, "data", "monitoring", "drift")
    os.makedirs(drift_dir, exist_ok=True)

    if not os.path.exists(data_raw_path):
        data_raw_path = os.path.join(base_dir, "data", "raw", "churn.csv")

    df = pd.read_csv(data_raw_path)
    evolved = df.copy()

    # Shift horsepower and curbweight up by 15-20% (modern vehicle specs)
    if 'horsepower' in evolved.columns:
        evolved['horsepower'] = (evolved['horsepower'] * 1.18).round().astype(int)
    if 'curbweight' in evolved.columns:
        evolved['curbweight'] = (evolved['curbweight'] * 1.12).round().astype(int)
    if 'price' in evolved.columns:
        evolved['price'] = (evolved['price'] * 1.25).round(2)

    unlabeled_path = os.path.join(drift_dir, "evolved_data.csv")
    labeled_path = os.path.join(drift_dir, "evolved_labeled_data.csv")

    evolved.to_csv(labeled_path, index=False)
    evolved.drop(columns=['price'], errors='ignore').to_csv(unlabeled_path, index=False)

    print(f"[STAGE 12] Created evolved datasets: {unlabeled_path} and {labeled_path}.")
    return True

if __name__ == "__main__":
    create_evolved_dataset()
