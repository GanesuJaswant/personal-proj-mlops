import os
import json
import time
from datetime import datetime, timezone

def log_inference(inference_id, input_payload, prediction, latency_ms):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(base_dir, "logs", "inference")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "inference_log.jsonl")

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "inference_id": inference_id,
        "input": input_payload,
        "prediction": prediction,
        "latency_ms": round(latency_ms, 3)
    }

    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as e:
        print(f"[ERROR] Failed writing inference log: {e}")
