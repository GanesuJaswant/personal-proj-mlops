import os
import json
import importlib

def run_full_drift_analysis():
    print("[STAGE 12] Running Comprehensive Drift & Stability Analysis Report...")
    
    data_drift_mod = importlib.import_module("src.mlops_pipeline.12_data_drift")
    concept_drift_mod = importlib.import_module("src.mlops_pipeline.12_concept_drift")
    
    data_drift_report = data_drift_mod.detect_data_drift()
    concept_drift_report = concept_drift_mod.detect_concept_drift()

    summary = {
        "status": "ANALYSIS_COMPLETE",
        "data_drift": data_drift_report,
        "concept_drift": concept_drift_report,
        "action_required": concept_drift_report["drift_detected"]
    }
    print(f"[STAGE 12] Full Drift Analysis Complete. Action Required: {summary['action_required']}")
    return summary

if __name__ == "__main__":
    run_full_drift_analysis()
