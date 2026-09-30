import subprocess
import sys
import os

def execute_pipeline():
    print("[INFO] =========================================")
    print("[INFO] Starting Lab 6: Model Registry & Lifecycle")
    print("[INFO] =========================================")
    
    # Ensure working from project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)
    
    scripts = [
        "src/train_registry.py",          # Trains and registers a new model version
        "src/automate_lifecycle.py",      # Compares versions and promotes Champion
        "src/generate_registry_report.py" # Generates the JSON deployment artifact
    ]
    
    for script in scripts:
        print(f"\n[INFO] ---> Executing {script}...")
        result = subprocess.run([sys.executable, script])
        
        if result.returncode != 0:
            print(f"[ERROR] Pipeline halted. {script} caught an error.")
            sys.exit(1)
            
    print("\n[SUCCESS] Lab 6 Model Registry Pipeline fully executed!")

if __name__ == "__main__":
    execute_pipeline()
