import sys
import mlflow
from mlflow.tracking import MlflowClient

def inspect_run(run_id=None):
    client = MlflowClient()
    if not run_id:
        if len(sys.argv) > 1:
            run_id = sys.argv[1]
        else:
            # Pick latest run from any experiment
            experiments = client.search_experiments()
            for exp in experiments:
                runs = client.search_runs(experiment_ids=[exp.experiment_id], max_results=1)
                if runs:
                    run_id = runs[0].info.run_id
                    break

    if not run_id:
        print("[ERROR] No run ID provided and no existing runs found.")
        return

    print(f"=== Inspecting MLflow Run: {run_id} ===")
    run = client.get_run(run_id)
    print(f"Experiment ID: {run.info.experiment_id}")
    print(f"Status:        {run.info.status}")
    print(f"Start Time:    {run.info.start_time}")
    print(f"End Time:      {run.info.end_time}")
    print(f"Artifact URI:  {run.info.artifact_uri}")
    
    print("\n--- Parameters ---")
    for k, v in run.data.params.items():
        print(f"  {k}: {v}")

    print("\n--- Metrics ---")
    for k, v in run.data.metrics.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, (int, float)) else f"  {k}: {v}")

    print("\n--- Tags ---")
    for k, v in run.data.tags.items():
        if not k.startswith("mlflow."):
            print(f"  {k}: {v}")

if __name__ == "__main__":
    inspect_run()
