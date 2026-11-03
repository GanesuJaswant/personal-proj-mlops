import os
import sys
import json
import time
import numpy as np
import joblib

def run_offline_inference():
    print("[STAGE 09] Running Offline Batch Inference on Test Data...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_processed_dir = os.path.join(base_dir, "data", "processed")
    models_dir = os.path.join(base_dir, "models")
    logs_dir = os.path.join(base_dir, "logs", "inference")
    os.makedirs(logs_dir, exist_ok=True)

    X_test = np.load(os.path.join(data_processed_dir, 'X_test_final.npy'))
    y_test = np.load(os.path.join(data_processed_dir, 'y_test.npy'))

    model_path = os.path.join(models_dir, "car_price_prediction_model.pkl")
    model = joblib.load(model_path)

    start_time = time.time()
    preds = model.predict(X_test)
    duration_ms = (time.time() - start_time) * 1000.0

    print(f"[STAGE 09] Generated {len(preds)} predictions in {duration_ms:.2f}ms.")
    print(f"[STAGE 09] Sample Prediction: ${preds[0]:,.2f} (Actual: ${y_test[0]:,.2f})")
    return preds

if __name__ == "__main__":
    run_offline_inference()
