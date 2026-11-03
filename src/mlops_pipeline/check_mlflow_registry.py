import mlflow
from mlflow.tracking import MlflowClient

def check_registry():
    client = MlflowClient()
    model_name = "Car_Price_Production_Model"

    print("=" * 60)
    print(f"MLFLOW MODEL REGISTRY CHECK: {model_name}")
    print("=" * 60)

    try:
        registered_model = client.get_registered_model(model_name)
        print(f"Model Name: {registered_model.name}")
        for v in registered_model.latest_versions:
            print(f"  Version: {v.version} | Current Stage: {v.current_stage:<12} | Run ID: {v.run_id[:8]}")
    except Exception as e:
        print(f"[INFO] Registry check: {e}")

if __name__ == "__main__":
    check_registry()
