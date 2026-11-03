import os
import mlflow
from mlflow.tracking import MlflowClient

def main():
    print("=" * 60)
    print("MLflow Tracking & Registry Status")
    print("=" * 60)
    
    client = MlflowClient()
    
    # 1. Experiments
    experiments = client.search_experiments()
    print(f"\n[INFO] Found {len(experiments)} Experiment(s):")
    for exp in experiments:
        print(f"  - ID: {exp.experiment_id} | Name: {exp.name} | Artifact Location: {exp.artifact_location}")
        runs = client.search_runs(experiment_ids=[exp.experiment_id], max_results=5)
        print(f"    Recent runs ({len(runs)}):")
        for r in runs:
            r2 = r.data.metrics.get("r2_score", "N/A")
            rmse = r.data.metrics.get("rmse", "N/A")
            print(f"      * Run ID: {r.info.run_id[:8]} | Status: {r.info.status} | R2: {r2} | RMSE: {rmse}")

    # 2. Registered Models
    registered_models = client.search_registered_models()
    print(f"\n[INFO] Found {len(registered_models)} Registered Model(s):")
    for rm in registered_models:
        print(f"\n  Model: {rm.name}")
        for mv in rm.latest_versions:
            print(f"    - Version: {mv.version} | Stage: {mv.current_stage} | Run ID: {mv.run_id[:8]}")

if __name__ == "__main__":
    main()
