import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error

def detect_concept_drift():
    print("[STAGE 12] Assessing Model Concept Drift (Performance Decay)...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    models_dir = os.path.join(base_dir, "models")
    evolved_labeled_path = os.path.join(base_dir, "data", "monitoring", "drift", "evolved_labeled_data.csv")

    model = joblib.load(os.path.join(models_dir, "car_price_prediction_model.pkl"))
    preprocessor = joblib.load(os.path.join(models_dir, "preprocessor.pkl"))

    df_drift = pd.read_csv(evolved_labeled_path)
    X = df_drift.drop(columns=['price'], errors='ignore')
    y_true = df_drift['price']

    # Preprocess
    for col in X.select_dtypes(include=['object', 'category', 'str']).columns:
        X[col] = X[col].astype(str).str.strip()

    if 'carbrand' not in X.columns:
        if 'CarName' in X.columns:
            X['carbrand'] = X['CarName'].str.split().str[0].str.lower()
        else:
            X['carbrand'] = "toyota"

    for drop_c in ['car_ID', 'CarName']:
        if drop_c in X.columns:
            X = X.drop(columns=[drop_c])

    X_mat = preprocessor.transform(X)
    y_pred = model.predict(X_mat)

    drift_r2 = float(r2_score(y_true, y_pred))
    drift_rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))

    baseline_r2 = 0.9124
    decay_pct = float(((baseline_r2 - drift_r2) / baseline_r2) * 100.0)

    print(f"[STAGE 12] Baseline R2: {baseline_r2:.4f} -> Drift Dataset R2: {drift_r2:.4f} (Decay: {decay_pct:.1f}%)")
    drift_detected = decay_pct > 5.0
    return {"drift_detected": drift_detected, "decay_percentage": decay_pct, "drift_r2": drift_r2}

if __name__ == "__main__":
    detect_concept_drift()
