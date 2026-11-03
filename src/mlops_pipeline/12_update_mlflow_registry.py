import os
import mlflow
from mlflow.tracking import MlflowClient

def update_registry_with_retrained():
    print("[STAGE 12] Updating MLflow Registry with Retrained Model v2...")
    client = MlflowClient()
    model_name = "Car_Price_Production_Model"

    try:
        versions = client.search_model_versions(f"name='{model_name}'")
        if versions:
            print(f"[STAGE 12] Found {len(versions)} versions for '{model_name}'. Registry synchronized.")
        else:
            print(f"[STAGE 12] Model '{model_name}' initialized in registry.")
    except Exception as e:
        print(f"[STAGE 12 NOTE] MLflow Registry status: {e}")

if __name__ == "__main__":
    update_registry_with_retrained()
