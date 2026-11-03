import os
import sys
import numpy as np

def validate_pipeline_outputs():
    print("[STAGE 04] Validating processed pipeline output arrays...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_processed_dir = os.path.join(base_dir, "data", "processed")

    try:
        X_train = np.load(os.path.join(data_processed_dir, 'X_train_final.npy'))
        X_test = np.load(os.path.join(data_processed_dir, 'X_test_final.npy'))
        y_train = np.load(os.path.join(data_processed_dir, 'y_train.npy'))
        y_test = np.load(os.path.join(data_processed_dir, 'y_test.npy'))
    except Exception as e:
        print(f"[STAGE 04 ERROR] Failed loading numpy arrays: {e}")
        sys.exit(1)

    errors = []

    # 1. Feature dimension parity
    if X_train.shape[1] != X_test.shape[1]:
        errors.append(f"Feature count mismatch: Train has {X_train.shape[1]}, Test has {X_test.shape[1]}")

    # 2. Row count alignment
    if X_train.shape[0] != y_train.shape[0]:
        errors.append(f"Train samples mismatch: X={X_train.shape[0]}, y={y_train.shape[0]}")
    if X_test.shape[0] != y_test.shape[0]:
        errors.append(f"Test samples mismatch: X={X_test.shape[0]}, y={y_test.shape[0]}")

    # 3. NaN or Inf check
    if np.isnan(X_train).any() or np.isnan(X_test).any():
        errors.append("NaN values detected in processed features.")
    if np.isinf(X_train).any() or np.isinf(X_test).any():
        errors.append("Infinite values detected in processed features.")

    if errors:
        print(f"[STAGE 04 FAILED] Output validation errors: {errors}")
        sys.exit(1)

    print(f"[STAGE 04] Output validation passed: Train={X_train.shape}, Test={X_test.shape}, NaNs=0, Infs=0.")
    return True

if __name__ == "__main__":
    validate_pipeline_outputs()
