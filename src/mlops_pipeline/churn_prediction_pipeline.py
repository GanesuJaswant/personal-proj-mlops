import os
import sys
import time
import json
from datetime import datetime, timezone
import subprocess

def run_pipeline():
    print("=" * 70)
    print(" EXECUTING END-TO-END MLOPS PRODUCTION PIPELINE")
    print("=" * 70)

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(base_dir)

    stages = [
        ("01_load_data", "src/mlops_pipeline/01_load_data.py"),
        ("02_validate_data", "src/mlops_pipeline/02_validate_data.py"),
        ("03_preprocessing", "src/mlops_pipeline/03_preprocessing.py"),
        ("04_validate_outputs", "src/mlops_pipeline/04_validate_outputs.py"),
        ("05_train_registry", "src/mlops_pipeline/05_train_registry.py"),
        ("06_model_evaluation", "src/mlops_pipeline/06_model_evaluation.py"),
        ("07_quality_gate", "src/mlops_pipeline/07_quality_gate.py"),
        ("08_automate_lifecycle", "src/mlops_pipeline/08_automate_lifecycle.py"),
        ("11_prepare_deployment", "src/mlops_pipeline/11_prepare_deployment.py")
    ]

    stage_logs = []
    overall_status = "SUCCESS"

    for stage_name, script_path in stages:
        print(f"\n[PIPELINE] ---> Running {stage_name} ({script_path})...")
        t0 = time.time()
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        dur = round(time.time() - t0, 3)

        if result.returncode != 0:
            print(f"[PIPELINE ERROR] Stage {stage_name} failed with error:")
            print(result.stderr)
            stage_logs.append({
                "stage": stage_name,
                "script": script_path,
                "status": "FAILED",
                "duration_s": dur,
                "error": result.stderr[:200]
            })
            overall_status = "FAILED"
            break
        else:
            print(f"[PIPELINE SUCCESS] Stage {stage_name} completed in {dur}s.")
            stage_logs.append({
                "stage": stage_name,
                "script": script_path,
                "status": "SUCCESS",
                "duration_s": dur
            })

    run_log = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stages": stage_logs,
        "overall_status": overall_status
    }

    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "churn_prediction_pipeline_run_log.json"), "w", encoding="utf-8") as f:
        json.dump(run_log, f, indent=4)
    with open(os.path.join(log_dir, "pipeline_run_log.json"), "w", encoding="utf-8") as f:
        json.dump(run_log, f, indent=4)

    if overall_status == "SUCCESS":
        print("\n[SUCCESS] Entire MLOps Pipeline executed and validated successfully!")
    else:
        print("\n[ERROR] Pipeline halted due to stage failure.")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
