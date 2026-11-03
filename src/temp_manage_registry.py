"""Helper utility to view and manage MLflow model registry stages."""
import sys
import mlflow
from mlflow.tracking import MlflowClient

def manage_registry():
    client = MlflowClient()
    model_name = "Car_Price_Production_Model"

    print(f"[INFO] Querying MLflow Model Registry for '{model_name}'...")
    try:
        registered_model = client.get_registered_model(model_name)
    except Exception as e:
        print(f"[WARNING] Model '{model_name}' not yet in registry: {e}")
        return

    print(f"Model: {registered_model.name}")
    for v in registered_model.latest_versions:
        print(f"  -> Version: {v.version} | Current Stage: {v.current_stage} | Run ID: {v.run_id[:8]}")

if __name__ == "__main__":
    manage_registry()
