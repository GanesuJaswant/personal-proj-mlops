"""Temporary test runner for API inference pipeline."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from api.model_loader import load_artifacts
from api.preprocessing import preprocess_input

sample_payload = {
    "symboling": 3,
    "carbrand": "alfa-romero",
    "fueltype": "gas",
    "aspiration": "std",
    "doornumber": "two",
    "carbody": "convertible",
    "drivewheel": "rwd",
    "enginelocation": "front",
    "wheelbase": 88.6,
    "carlength": 168.8,
    "carwidth": 64.1,
    "carheight": 48.8,
    "curbweight": 2548,
    "enginetype": "dohc",
    "cylindernumber": "four",
    "enginesize": 130,
    "fuelsystem": "mpfi",
    "boreratio": 3.47,
    "stroke": 2.68,
    "compressionratio": 9.0,
    "horsepower": 111,
    "peakrpm": 5000,
    "citympg": 21,
    "highwaympg": 27
}

def test_inference_flow():
    print("[TEST] Loading model and preprocessor...")
    model, preprocessor = load_artifacts()
    print("[TEST] Running preprocessing...")
    X_vec = preprocess_input(sample_payload, preprocessor)
    print(f"[TEST] Processed feature vector shape: {X_vec.shape}")
    pred = model.predict(X_vec)
    print(f"[TEST] Predicted car price: ${pred[0]:,.2f}")

if __name__ == "__main__":
    test_inference_flow()
