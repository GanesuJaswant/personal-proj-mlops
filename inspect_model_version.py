import sys
import mlflow
from mlflow.tracking import MlflowClient

def inspect_version(model_name="Car_Price_Production_Model", version=None):
    if len(sys.argv) > 1:
        model_name = sys.argv[1]
    if len(sys.argv) > 2:
        version = sys.argv[2]

    client = MlflowClient()
    try:
        registered_model = client.get_registered_model(model_name)
    except Exception as e:
        print(f"[ERROR] Could not find registered model '{model_name}': {e}")
        return

    print(f"=== Registered Model: {registered_model.name} ===")
    print(f"Description: {registered_model.description}")
    
    versions = registered_model.latest_versions if not version else [client.get_model_version(model_name, version)]
    for v in versions:
        print(f"\n--- Version {v.version} ---")
        print(f"Stage:            {v.current_stage}")
        print(f"Status:           {v.status}")
        print(f"Run ID:           {v.run_id}")
        print(f"Source:           {v.source}")
        print(f"Created:          {v.creation_timestamp}")
        print(f"Last Updated:     {v.last_updated_timestamp}")
        
        # Fetch associated run metrics
        try:
            run = client.get_run(v.run_id)
            print("Run Metrics:")
            for m_key, m_val in run.data.metrics.items():
                print(f"  * {m_key}: {m_val}")
        except Exception:
            pass

if __name__ == "__main__":
    inspect_version()
