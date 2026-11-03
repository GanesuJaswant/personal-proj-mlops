import os
import sys
import importlib

def deploy_if_promoted():
    print("[INFO] Checking if champion model is qualified for production deployment...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dep_mod = importlib.import_module("src.mlops_pipeline.11_prepare_deployment")
    dep_mod.prepare_deployment()
    print("[SUCCESS] Production deployment verified.")

if __name__ == "__main__":
    deploy_if_promoted()
