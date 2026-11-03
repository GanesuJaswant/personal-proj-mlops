import os
import json

def analyze_request_history():
    print("[STAGE 12] Analyzing Historical Request Distribution & Frequency...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_path = os.path.join(base_dir, "logs", "inference", "inference_log.jsonl")

    brands = {}
    total = 0
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        record = json.loads(line)
                        total += 1
                        brand = record.get("input", {}).get("carbrand", "unknown")
                        brands[brand] = brands.get(brand, 0) + 1
                    except Exception:
                        pass

    print(f"[STAGE 12] Analyzed {total} requests. Most frequent brands: {brands}")
    return {"total_requests": total, "brand_breakdown": brands}

if __name__ == "__main__":
    analyze_request_history()
