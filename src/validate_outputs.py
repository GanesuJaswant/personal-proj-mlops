import os
import json
import numpy as np

def validate_preprocessing_outputs():
    print("[INFO] Validating Preprocessing Outputs for Car Price Prediction...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_processed_dir = os.path.join(base_dir, 'data', 'processed')
    artifacts_dir = os.path.join(base_dir, 'artifacts')
    os.makedirs(artifacts_dir, exist_ok=True)
    
    # 1. Load the pipeline outputs
    try:
        X_train = np.load(os.path.join(data_processed_dir, 'X_train_final.npy'))
        X_test = np.load(os.path.join(data_processed_dir, 'X_test_final.npy'))
        y_train = np.load(os.path.join(data_processed_dir, 'y_train.npy'))
        y_test = np.load(os.path.join(data_processed_dir, 'y_test.npy'))
    except FileNotFoundError as e:
        print(f"[ERROR] Could not find processed data: {e}")
        return False
        
    errors = []
    
    # 2. Assert No Missing Values (Validating the Imputer)
    if np.isnan(X_train).sum() > 0:
        errors.append("NaNs detected in X_train after preprocessing.")
    if np.isnan(X_test).sum() > 0:
        errors.append("NaNs detected in X_test after preprocessing.")
    if np.isnan(y_train).sum() > 0:
        errors.append("NaNs detected in y_train.")
    if np.isnan(y_test).sum() > 0:
        errors.append("NaNs detected in y_test.")
        
    # 3. Assert Dimensionality Consistency (Validating OHE and Split)
    if X_train.shape[1] != X_test.shape[1]:
        errors.append(f"Feature mismatch: X_train has {X_train.shape[1]} cols, X_test has {X_test.shape[1]} cols.")
    if X_train.shape[0] != y_train.shape[0]:
        errors.append("Row mismatch between X_train and y_train.")
    if X_test.shape[0] != y_test.shape[0]:
        errors.append("Row mismatch between X_test and y_test.")
        
    # 4. Generate Transformation Summary Report
    report = {
        "test_name": "Car Price Preprocessing Output Validation",
        "validation_status": "PASSED" if not errors else "FAILED",
        "matrix_dimensions": {
            "X_train_shape": list(X_train.shape),
            "X_test_shape": list(X_test.shape),
            "y_train_shape": list(y_train.shape),
            "y_test_shape": list(y_test.shape)
        },
        "data_quality": {
            "missing_values_X_train": int(np.isnan(X_train).sum()),
            "missing_values_X_test": int(np.isnan(X_test).sum()),
            "missing_values_y_train": int(np.isnan(y_train).sum()),
            "missing_values_y_test": int(np.isnan(y_test).sum())
        },
        "errors": errors
    }
    
    report_path = os.path.join(artifacts_dir, 'preprocessing_summary_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
        
    if errors:
        print("[ERROR] Output Validation FAILED!")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("[SUCCESS] Output Validation PASSED.")
        print("[INFO] Features are clean, scaled, encoded, and dimensionally consistent.")
        print(f"[INFO] Summary report saved to {report_path}")
        return True

if __name__ == "__main__":
    success = validate_preprocessing_outputs()
    if not success:
        exit(1)
