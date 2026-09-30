import os
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def run_evaluation():
    print("Starting Model Evaluation...")
    
    # Determine base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_raw_dir = os.path.join(base_dir, 'data', 'raw')
    data_processed_dir = os.path.join(base_dir, 'data', 'processed')
    models_dir = os.path.join(base_dir, 'models')
    outputs_dir = os.path.join(base_dir, 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    
    # 1. Load test data and the trained model
    X_test_final = np.load(os.path.join(data_processed_dir, 'X_test_final.npy'))
    y_test = np.load(os.path.join(data_processed_dir, 'y_test.npy'))
    
    model_path = os.path.join(models_dir, 'random_forest_baseline.pkl')
    model = joblib.load(model_path)
    
    # 2. Make predictions
    y_pred = model.predict(X_test_final)
    
    # 3. Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print("\n--- Model Evaluation Report ---")
    print(f"MAE      : {mae:.2f}")
    print(f"RMSE     : {rmse:.2f}")
    print(f"R2-Score : {r2:.4f}")
    print("-------------------------------\n")
    
    # Save metrics JSON
    metrics = {
        "test_mae": float(mae),
        "test_rmse": float(rmse),
        "test_r2": float(r2)
    }
    metrics_path = os.path.join(outputs_dir, 'metrics.json')
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"Metrics saved to {metrics_path}")
    
    # 4. Error Analysis Export
    # Load raw data to map original car records back
    data_path = os.path.join(data_raw_dir, 'CarPrice_Assignment.csv')
    if not os.path.exists(data_path):
        data_path = os.path.join(base_dir, 'data', 'CarPrice_Assignment.csv')
        
    df = pd.read_csv(data_path)
    if 'CarName' in df.columns:
        df['carbrand'] = df['CarName'].str.split().str[0].str.lower()
        brand_corrections = {
            "maxda": "mazda", "porcshce": "porsche", "toyouta": "toyota",
            "vokswagen": "volkswagen", "vw": "volkswagen"
        }
        df['carbrand'] = df['carbrand'].replace(brand_corrections)
    
    cols_to_drop = [c for c in ['car_ID', 'CarName'] if c in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        
    _, X_test_raw = train_test_split(
        df.drop('price', axis=1), test_size=0.2, random_state=42
    )
    
    errors_df = X_test_raw.copy()
    errors_df['Actual_Price'] = y_test
    errors_df['Predicted_Price'] = y_pred
    errors_df['Residual'] = y_test - y_pred
    errors_df['Absolute_Error'] = np.abs(y_test - y_pred)
    errors_df['Percentage_Error'] = (errors_df['Absolute_Error'] / errors_df['Actual_Price']) * 100
    
    # Isolate overpredictions and underpredictions
    overpredictions = errors_df[errors_df['Predicted_Price'] > errors_df['Actual_Price']].sort_values(by='Absolute_Error', ascending=False)
    underpredictions = errors_df[errors_df['Predicted_Price'] < errors_df['Actual_Price']].sort_values(by='Absolute_Error', ascending=False)
    
    # Isolate top residual errors
    error_threshold = errors_df['Absolute_Error'].quantile(0.75)
    high_residual_errors = errors_df[errors_df['Absolute_Error'] >= error_threshold].sort_values(by='Absolute_Error', ascending=False)
    
    overpredictions.to_csv(os.path.join(outputs_dir, 'overpredictions.csv'), index=False)
    underpredictions.to_csv(os.path.join(outputs_dir, 'underpredictions.csv'), index=False)
    high_residual_errors.to_csv(os.path.join(outputs_dir, 'high_residual_errors.csv'), index=False)
    
    print("Evaluation complete and error analysis files saved to outputs folder!")

if __name__ == "__main__":
    run_evaluation()
