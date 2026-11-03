import os
import sys
import json
import pandas as pd

# Allow importing local pipeline modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.mlops_pipeline.validation import check_missing_columns, check_negative_values, check_null_values

def validate_raw_data():
    print("[STAGE 02] Validating raw dataset schema and integrity...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_path = os.path.join(base_dir, "data", "raw", "CarPrice_Assignment.csv")
    artifacts_dir = os.path.join(base_dir, "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)

    if not os.path.exists(data_path):
        data_path = os.path.join(base_dir, "data", "raw", "churn.csv")

    df = pd.read_csv(data_path)
    errors = []

    if len(df) == 0:
        errors.append("Dataset is empty.")

    missing = check_missing_columns(df)
    if missing:
        errors.append(f"Missing columns: {missing}")

    negatives = check_negative_values(df)
    if negatives:
        errors.append(f"Negative values detected in positive numerical columns: {negatives}")

    nulls = check_null_values(df)
    if nulls:
        errors.append(f"Unexpected null values in raw file: {nulls}")

    status = "PASSED" if not errors else "FAILED"
    report = {
        "validation_status": status,
        "total_records_checked": len(df),
        "errors_detected": errors,
        "error_count": len(errors)
    }

    report_path = os.path.join(artifacts_dir, "data_validation_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    if status == "FAILED":
        print(f"[STAGE 02] Data Validation FAILED with errors: {errors}")
        sys.exit(1)

    print("[STAGE 02] Data validation passed successfully with 0 schema violations.")
    return True

if __name__ == "__main__":
    validate_raw_data()
