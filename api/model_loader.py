import os
import joblib

_MODEL = None
_PREPROCESSOR = None

def get_base_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_artifacts():
    global _MODEL, _PREPROCESSOR
    if _MODEL is not None and _PREPROCESSOR is not None:
        return _MODEL, _PREPROCESSOR

    base_dir = get_base_dir()

    # Model candidates in order of priority
    model_paths = [
        os.path.join(base_dir, "deployment", "model.pkl"),
        os.path.join(base_dir, "models", "car_price_prediction_model.pkl"),
        os.path.join(base_dir, "models", "random_forest_baseline.pkl"),
        os.path.join(base_dir, "models", "random_forest_mlflow.pkl"),
        os.path.join(base_dir, "models", "churn_model.pkl")
    ]

    preprocessor_paths = [
        os.path.join(base_dir, "deployment", "preprocessor.pkl"),
        os.path.join(base_dir, "models", "preprocessor.pkl")
    ]

    # Load model
    for p in model_paths:
        if os.path.exists(p):
            try:
                _MODEL = joblib.load(p)
                print(f"[INFO] Loaded model from: {p}")
                break
            except Exception as e:
                print(f"[WARNING] Failed loading model {p}: {e}")

    # Load preprocessor
    for p in preprocessor_paths:
        if os.path.exists(p):
            try:
                _PREPROCESSOR = joblib.load(p)
                print(f"[INFO] Loaded preprocessor from: {p}")
                break
            except Exception as e:
                print(f"[WARNING] Failed loading preprocessor {p}: {e}")

    if _MODEL is None or _PREPROCESSOR is None:
        raise RuntimeError("Failed to load required model and preprocessor artifacts.")

    return _MODEL, _PREPROCESSOR
