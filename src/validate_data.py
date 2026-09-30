import os
import json
import pandas as pd
import numpy as np

def run_data_validation():
    print("[INFO] Starting Raw Data Validation for Car Price Prediction...")
    
    # Check data path
    data_path = 'data/raw/CarPrice_Assignment.csv'
    if not os.path.exists(data_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fallback = os.path.join(base_dir, 'data', 'raw', 'CarPrice_Assignment.csv')
        if os.path.exists(fallback):
            data_path = fallback
        else:
            fallback2 = os.path.join(base_dir, 'data', 'CarPrice_Assignment.csv')
            if os.path.exists(fallback2):
                data_path = fallback2
            else:
                print(f"[ERROR] Data file not found at {data_path}")
                return False
        
    df = pd.read_csv(data_path)
    errors = []
    
    # 1. Check Row Count
    if len(df) == 0:
        errors.append("Dataset is empty.")
        
    # 2. Check Expected Columns
    required_columns = [
        'car_ID', 'symboling', 'CarName', 'fueltype', 'aspiration',
        'doornumber', 'carbody', 'drivewheel', 'enginelocation',
        'wheelbase', 'carlength', 'carwidth', 'carheight', 'curbweight',
        'enginetype', 'cylindernumber', 'enginesize', 'fuelsystem',
        'boreratio', 'stroke', 'compressionratio', 'horsepower',
        'peakrpm', 'citympg', 'highwaympg', 'price'
    ]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
        
    # 3. Check Value Constraints
    if 'price' in df.columns:
        invalid_price = df[df['price'] <= 0]
        if len(invalid_price) > 0:
            errors.append(f"Invalid non-positive car price found: {len(invalid_price)} rows.")
            
    if 'enginesize' in df.columns:
        invalid_engine = df[df['enginesize'] <= 0]
        if len(invalid_engine) > 0:
            errors.append(f"Invalid non-positive enginesize found: {len(invalid_engine)} rows.")
            
    if 'horsepower' in df.columns:
        invalid_hp = df[df['horsepower'] <= 0]
        if len(invalid_hp) > 0:
            errors.append(f"Invalid non-positive horsepower found: {len(invalid_hp)} rows.")
            
    if 'curbweight' in df.columns:
        invalid_weight = df[df['curbweight'] <= 0]
        if len(invalid_weight) > 0:
            errors.append(f"Invalid non-positive curbweight found: {len(invalid_weight)} rows.")
            
    if 'wheelbase' in df.columns:
        invalid_wb = df[df['wheelbase'] <= 0]
        if len(invalid_wb) > 0:
            errors.append(f"Invalid non-positive wheelbase found: {len(invalid_wb)} rows.")
            
    # 4. Generate Validation Report
    report = {
        "test_name": "Car Price Raw Data Validation",
        "validation_status": "PASSED" if not errors else "FAILED",
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "columns_checked": required_columns,
        "errors": errors
    }
    
    os.makedirs("artifacts", exist_ok=True)
    report_path = 'artifacts/data_validation_report.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
        
    if errors:
        print("[ERROR] Data Validation FAILED:")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print(f"[SUCCESS] Data Validation PASSED! Verified {len(df)} records.")
        print(f"[INFO] Report saved to {report_path}")
        return True

if __name__ == "__main__":
    success = run_data_validation()
    if not success:
        exit(1)
