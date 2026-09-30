import os
import json
import mlflow
from mlflow.tracking import MlflowClient

def generate_registry_report():
    print("[INFO] Generating Model Registry Report for Car Price Prediction...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    artifacts_dir = os.path.join(base_dir, 'artifacts')
    os.makedirs(artifacts_dir, exist_ok=True)
    
    client = MlflowClient()
    model_name = "Car_Price_Production_Model"
    
    try:
        # Search for the model specifically in Production
        production_models = client.search_model_versions(f"name='{model_name}'")
        champion = next((mv for mv in production_models if mv.current_stage == "Production"), None)
        
        if not champion:
            print("[ERROR] No model found in Production stage!")
            return False
            
        # Get run details
        run = client.get_run(champion.run_id)
        
        # Build deployment report
        report = {
            "registry_status": "READY_FOR_DEPLOYMENT",
            "model_lineage": {
                "registered_name": model_name,
                "version": int(champion.version),
                "current_stage": champion.current_stage,
                "run_id": champion.run_id,
                "artifact_uri": champion.source
            },
            "performance_metrics": {
                "r2_score": run.data.metrics.get("r2_score"),
                "rmse": run.data.metrics.get("rmse"),
                "mae": run.data.metrics.get("mae"),
                "mse": run.data.metrics.get("mse")
            },
            "hyperparameters": run.data.params,
            "preprocessing_dependency": "models/preprocessor.pkl"
        }
        
        report_path = os.path.join(artifacts_dir, "production_model_report.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=4)
            
        print(f"[SUCCESS] Report successfully generated for Production Model Version {champion.version}")
        print(f"[INFO] Saved to: {report_path}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to generate report: {e}")
        return False

if __name__ == "__main__":
    success = generate_registry_report()
    if not success:
        exit(1)
