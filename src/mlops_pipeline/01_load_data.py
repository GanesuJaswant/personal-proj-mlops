import os
import json
import time
import pandas as pd

def load_data():
    print("[STAGE 01] Loading raw dataset...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_path = os.path.join(base_dir, "data", "raw", "CarPrice_Assignment.csv")
    artifacts_dir = os.path.join(base_dir, "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)

    if not os.path.exists(data_path):
        fallback = os.path.join(base_dir, "data", "raw", "churn.csv")
        if os.path.exists(fallback):
            data_path = fallback
        else:
            raise FileNotFoundError(f"Raw data file not found at {data_path}")

    start_time = time.time()
    df = pd.read_csv(data_path)
    duration_ms = (time.time() - start_time) * 1000.0

    report = {
        "source_file": data_path,
        "total_rows": int(df.shape[0]),
        "total_columns": int(df.shape[1]),
        "file_size_bytes": os.path.getsize(data_path),
        "column_types": {
            "numerical": int(len(df.select_dtypes(include=['int64', 'float64']).columns)),
            "categorical": int(len(df.select_dtypes(include=['object', 'category']).columns))
        },
        "load_duration_ms": round(duration_ms, 2),
        "status": "SUCCESS"
    }

    report_path = os.path.join(artifacts_dir, "data_load_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print(f"[STAGE 01] Successfully loaded {len(df)} rows, {df.shape[1]} columns. Report saved to {report_path}.")
    return df

if __name__ == "__main__":
    load_data()
