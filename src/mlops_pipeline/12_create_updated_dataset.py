import os
import pandas as pd

def create_updated_dataset():
    print("[STAGE 12] Aggregating Historical Data with Evolved Observations...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    train_path = os.path.join(base_dir, "data", "processed", "train_dataset.csv")
    evolved_path = os.path.join(base_dir, "data", "monitoring", "drift", "evolved_labeled_data.csv")
    out_path = os.path.join(base_dir, "data", "processed", "updated_training_data.csv")

    df_train = pd.read_csv(train_path)
    df_evolved = pd.read_csv(evolved_path).sample(frac=0.5, random_state=42)

    updated = pd.concat([df_train, df_evolved], ignore_index=True)
    updated.to_csv(out_path, index=False)
    print(f"[STAGE 12] Updated training dataset saved to {out_path} with {len(updated)} total records.")
    return True

if __name__ == "__main__":
    create_updated_dataset()
