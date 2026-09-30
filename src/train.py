import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor

def run_training():
    print("Starting Model Training for Car Price Prediction...")
    
    # Determine base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_processed_dir = os.path.join(base_dir, 'data', 'processed')
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # 1. Load processed training data
    X_train_final = np.load(os.path.join(data_processed_dir, 'X_train_final.npy'))
    y_train = np.load(os.path.join(data_processed_dir, 'y_train.npy'))
    
    # 2. Train Decision Tree Baseline
    print("Training Decision Tree Baseline...")
    dt_model = DecisionTreeRegressor(max_depth=5, random_state=42)
    dt_model.fit(X_train_final, y_train)
    dt_path = os.path.join(models_dir, 'decision_tree_baseline.pkl')
    joblib.dump(dt_model, dt_path)
    print(f"Decision Tree saved to {dt_path}")
    
    # 3. Train Random Forest Baseline
    print("Training Random Forest Baseline...")
    rf_model = RandomForestRegressor(
        n_estimators=100, 
        max_depth=10, 
        random_state=42
    )
    rf_model.fit(X_train_final, y_train)
    rf_path = os.path.join(models_dir, 'random_forest_baseline.pkl')
    joblib.dump(rf_model, rf_path)
    print(f"Random Forest saved to {rf_path}")
    
    print("Model training complete and saved to disk!")

if __name__ == "__main__":
    run_training()
