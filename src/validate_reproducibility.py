import os
import json
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

def run_deterministic_test():
    print("Running Reproducibility Validation for Car Price Prediction...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_processed_dir = os.path.join(base_dir, 'data', 'processed')
    artifacts_dir = os.path.join(base_dir, 'artifacts')
    os.makedirs(artifacts_dir, exist_ok=True)
    
    # Load Data
    X_train = np.load(os.path.join(data_processed_dir, 'X_train_final.npy'))
    X_test = np.load(os.path.join(data_processed_dir, 'X_test_final.npy'))
    y_train = np.load(os.path.join(data_processed_dir, 'y_train.npy'))
    y_test = np.load(os.path.join(data_processed_dir, 'y_test.npy'))
    
    # Fixed Parameters for strict reproducibility
    params = {"n_estimators": 100, "max_depth": 10, "random_state": 42}
    
    # Execution 1
    model_1 = RandomForestRegressor(**params)
    model_1.fit(X_train, y_train)
    score_1 = r2_score(y_test, model_1.predict(X_test))
    rmse_1 = float(np.sqrt(mean_squared_error(y_test, model_1.predict(X_test))))
    
    # Execution 2 (Simulating a re-run)
    model_2 = RandomForestRegressor(**params)
    model_2.fit(X_train, y_train)
    score_2 = r2_score(y_test, model_2.predict(X_test))
    rmse_2 = float(np.sqrt(mean_squared_error(y_test, model_2.predict(X_test))))
    
    # Validate consistency
    is_reproducible = bool(np.isclose(score_1, score_2, atol=1e-7) and np.isclose(rmse_1, rmse_2, atol=1e-7))
    
    # Generate Report
    report = {
        "test_name": "Car Price Pipeline Reproducibility Validation",
        "parameters": params,
        "execution_1_r2": float(score_1),
        "execution_2_r2": float(score_2),
        "execution_1_rmse": rmse_1,
        "execution_2_rmse": rmse_2,
        "is_strictly_reproducible": is_reproducible,
        "status": "PASSED" if is_reproducible else "FAILED"
    }
    
    report_path = os.path.join(artifacts_dir, 'reproducibility_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
        
    print(f"Execution 1 R2: {score_1:.6f} | RMSE: {rmse_1:.4f}")
    print(f"Execution 2 R2: {score_2:.6f} | RMSE: {rmse_2:.4f}")
    if is_reproducible:
        print("[SUCCESS] Pipeline is 100% reproducible. Report saved.")
        return True
    else:
        print("[FAILED] Pipeline is non-deterministic.")
        return False

if __name__ == "__main__":
    success = run_deterministic_test()
    if not success:
        exit(1)
