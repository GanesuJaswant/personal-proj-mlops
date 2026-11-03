import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score

def compare_champion_vs_retrained():
    print("[STAGE 12] Tournament: Champion v1 vs Retrained Challenger v2...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    models_dir = os.path.join(base_dir, "models")
    test_path = os.path.join(base_dir, "data", "processed", "test_dataset.csv")

    m1 = joblib.load(os.path.join(models_dir, "car_price_prediction_model.pkl"))
    prep1 = joblib.load(os.path.join(models_dir, "preprocessor.pkl"))

    m2 = joblib.load(os.path.join(models_dir, "retrained_model_v2.pkl"))
    prep2 = joblib.load(os.path.join(models_dir, "retrained_preprocessor_v2.pkl"))

    df_test = pd.read_csv(test_path)
    for col in df_test.select_dtypes(include=['object', 'category', 'str']).columns:
        df_test[col] = df_test[col].astype(str).str.strip()

    if 'carbrand' not in df_test.columns:
        if 'CarName' in df_test.columns:
            df_test['carbrand'] = df_test['CarName'].str.split().str[0].str.lower()
        else:
            df_test['carbrand'] = "toyota"

    X = df_test.drop(columns=['price', 'car_ID', 'CarName'], errors='ignore')
    y = df_test['price']

    r2_v1 = float(r2_score(y, m1.predict(prep1.transform(X))))
    r2_v2 = float(r2_score(y, m2.predict(prep2.transform(X))))

    print(f"[STAGE 12] Comparison: Champion v1 R2={r2_v1:.4f} vs Challenger v2 R2={r2_v2:.4f}")
    promoted = r2_v2 >= r2_v1
    return {"champion_r2": r2_v1, "challenger_r2": r2_v2, "promote_challenger": promoted}

if __name__ == "__main__":
    compare_champion_vs_retrained()
