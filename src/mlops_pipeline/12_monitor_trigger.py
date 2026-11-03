import os
import sys
import importlib

def evaluate_trigger():
    print("[STAGE 12] Evaluating Automated Retraining Trigger Conditions...")
    concept_drift_mod = importlib.import_module("src.mlops_pipeline.12_concept_drift")
    res = concept_drift_mod.detect_concept_drift()

    if res["drift_detected"]:
        print("[TRIGGER FIRED] Concept drift decay exceeds 5.0%! Retraining Pipeline Triggered.")
        return True
    else:
        print("[TRIGGER STANDBY] System stable. No retraining necessary.")
        return False

if __name__ == "__main__":
    evaluate_trigger()
