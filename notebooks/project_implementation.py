"""
Car Price Prediction - Exploratory Data Analysis, Feature Engineering & Baseline Model Tournament
Converted from interactive Jupyter notebook into standalone production Python script.
"""

import os
import json
import joblib
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

warnings.filterwarnings('ignore')

def main():
    print("=" * 70)
    print(" CAR PRICE PREDICTION - EDA & MODELING PIPELINE (.py execution)")
    print("=" * 70)
    
    # 1. Base directories setup
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_raw_dir = os.path.join(base_dir, 'data', 'raw')
    data_processed_dir = os.path.join(base_dir, 'data', 'processed')
    models_dir = os.path.join(base_dir, 'models')
    outputs_dir = os.path.join(base_dir, 'outputs')
    
    for d in [data_processed_dir, models_dir, outputs_dir]:
        os.makedirs(d, exist_ok=True)
        
    # 2. Load dataset
    data_path = os.path.join(data_raw_dir, 'CarPrice_Assignment.csv')
    if not os.path.exists(data_path):
        data_path = os.path.join(base_dir, 'data', 'CarPrice_Assignment.csv')
        
    df = pd.read_csv(data_path)
    print(f"\n[INFO] Loaded dataset successfully: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # 3. Target Distribution Analysis
    print("\n--- Target Price Distribution Summary ---")
    print(df["price"].describe())
    print(f"Lowest 3 prices : {df['price'].nsmallest(3).tolist()}")
    print(f"Highest 3 prices: {df['price'].nlargest(3).tolist()}")
    
    # 4. Data Cleaning & Feature Extraction
    print("\n[INFO] Cleaning data and extracting brand names...")
    for col in df.select_dtypes(include=['object', 'category', 'str']).columns:
        df[col] = df[col].astype(str).str.strip()
        
    if 'CarName' in df.columns:
        df['carbrand'] = df['CarName'].str.split().str[0].str.lower()
        brand_corrections = {
            "maxda": "mazda",
            "porcshce": "porsche",
            "toyouta": "toyota",
            "vokswagen": "volkswagen",
            "vw": "volkswagen"
        }
        df['carbrand'] = df['carbrand'].replace(brand_corrections)
        print(f"[INFO] Standardized {df['carbrand'].nunique()} unique car brands.")
        
    cols_to_drop = [c for c in ['car_ID', 'CarName'] if c in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        
    df = df.dropna()
    
    # 5. Train-Test Split (Splitting first to avoid data leakage)
    X = df.drop('price', axis=1)
    y = df['price']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"[INFO] Train split: {X_train.shape}, Test split: {X_test.shape}")
    
    # 6. Feature Encoding & Scaling
    cat_cols = X_train.select_dtypes(include=['object', 'category', 'str']).columns.tolist()
    num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(X_train[num_cols])
    x_test_scaled = scaler.transform(X_test[num_cols])
    
    ohe = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')
    x_train_encoded = ohe.fit_transform(X_train[cat_cols])
    x_test_encoded = ohe.transform(X_test[cat_cols])
    
    X_train_final = np.hstack((x_train_scaled, x_train_encoded))
    X_test_final = np.hstack((x_test_scaled, x_test_encoded))
    
    # Save artifacts
    np.save(os.path.join(data_processed_dir, 'X_train_final.npy'), X_train_final)
    np.save(os.path.join(data_processed_dir, 'X_test_final.npy'), X_test_final)
    np.save(os.path.join(data_processed_dir, 'y_train.npy'), y_train.to_numpy(dtype=np.float64))
    np.save(os.path.join(data_processed_dir, 'y_test.npy'), y_test.to_numpy(dtype=np.float64))
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
    joblib.dump(ohe, os.path.join(models_dir, 'ohe.pkl'))
    
    # 7. Model Evaluation Tournament
    print("\n" + "=" * 50)
    print(" MODEL TOURNAMENT EVALUATION")
    print("=" * 50)
    
    candidate_models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(alpha=1.0),
        'Decision Tree': DecisionTreeRegressor(max_depth=5, random_state=42),
        'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42)
    }
    
    results = []
    trained_models = {}
    
    for name, model in candidate_models.items():
        model.fit(X_train_final, y_train)
        preds = model.predict(X_test_final)
        mae = mean_absolute_error(y_test, preds)
        rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
        r2 = r2_score(y_test, preds)
        
        results.append({
            "Model": name,
            "MAE ($)": round(mae, 2),
            "RMSE ($)": round(rmse, 2),
            "R2-Score": round(r2, 4)
        })
        trained_models[name] = model
        
    results_df = pd.DataFrame(results).sort_values(by="R2-Score", ascending=False)
    print(results_df.to_string(index=False))
    
    best_model_name = results_df.iloc[0]["Model"]
    best_model = trained_models[best_model_name]
    best_r2 = results_df.iloc[0]["R2-Score"]
    print(f"\n[WINNER] Best Performing Model: {best_model_name} (R2: {best_r2})")
    
    # Save best model and baseline
    joblib.dump(trained_models['Random Forest'], os.path.join(models_dir, 'random_forest_baseline.pkl'))
    joblib.dump(trained_models['Decision Tree'], os.path.join(models_dir, 'decision_tree_baseline.pkl'))
    joblib.dump(best_model, os.path.join(models_dir, 'car_price_prediction_model.pkl'))
    
    # 8. Feature Importance for Tree Models
    if hasattr(best_model, "feature_importances_"):
        encoded_cat_names = ohe.get_feature_names_out(cat_cols)
        all_features = list(num_cols) + list(encoded_cat_names)
        importances = pd.Series(best_model.feature_importances_, index=all_features)
        top_10 = importances.sort_values(ascending=False).head(10)
        print("\n--- Top 10 Most Important Features ---")
        for feat, val in top_10.items():
            print(f"  {feat:<25}: {val:.4f}")
            
    print("\n[SUCCESS] Implementation script finished successfully!")

if __name__ == "__main__":
    main()
