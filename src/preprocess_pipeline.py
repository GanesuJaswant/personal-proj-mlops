import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def run_preprocessing():
    print("[INFO] Starting Sklearn Pipeline Preprocessing for Car Price Prediction...")
    
    # 1. Determine base directories
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_raw_dir = os.path.join(base_dir, 'data', 'raw')
    data_processed_dir = os.path.join(base_dir, 'data', 'processed')
    models_dir = os.path.join(base_dir, 'models')
    
    os.makedirs(data_processed_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    
    # Load raw data
    data_path = os.path.join(data_raw_dir, 'CarPrice_Assignment.csv')
    if not os.path.exists(data_path):
        fallback = os.path.join(base_dir, 'data', 'CarPrice_Assignment.csv')
        if os.path.exists(fallback):
            data_path = fallback
            
    df = pd.read_csv(data_path)
    print(f"[INFO] Loaded raw dataset with shape: {df.shape}")
    
    # 2. Data Cleaning & Feature Extraction
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
        
    cols_to_drop = [c for c in ['car_ID', 'CarName'] if c in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        
    df = df.dropna()
    df.to_csv(os.path.join(data_processed_dir, 'processed_dataset.csv'), index=False)
    
    # Separate features and target
    X = df.drop('price', axis=1)
    y = df['price']
    
    # 3. Train-Test Split (Done before transformations to prevent data leakage)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    train_df = df.loc[X_train.index]
    test_df = df.loc[X_test.index]
    train_df.to_csv(os.path.join(data_processed_dir, 'train_dataset.csv'), index=False)
    test_df.to_csv(os.path.join(data_processed_dir, 'test_dataset.csv'), index=False)
    test_df.to_csv(os.path.join(data_processed_dir, 'validation_dataset.csv'), index=False)
    
    # 4. Separate Column Types
    cat_cols = X_train.select_dtypes(include=['object', 'category', 'str']).columns.tolist()
    num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    # 5. Build Modular Scikit-Learn Pipelines
    num_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    cat_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('ohe', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_pipeline, num_cols),
            ('cat', cat_pipeline, cat_cols)
        ]
    )
    
    # 6. Execute Pipeline
    print("[INFO] Fitting and transforming training data...")
    X_train_final = preprocessor.fit_transform(X_train)
    
    print("[INFO] Transforming test data...")
    X_test_final = preprocessor.transform(X_test)
    
    # 7. Save Artifacts
    np.save(os.path.join(data_processed_dir, 'X_train_final.npy'), X_train_final)
    np.save(os.path.join(data_processed_dir, 'X_test_final.npy'), X_test_final)
    np.save(os.path.join(data_processed_dir, 'y_train.npy'), y_train.to_numpy(dtype=np.float64))
    np.save(os.path.join(data_processed_dir, 'y_test.npy'), y_test.to_numpy(dtype=np.float64))
    
    # Save the single preprocessor artifact
    preprocessor_path = os.path.join(models_dir, 'preprocessor.pkl')
    joblib.dump(preprocessor, preprocessor_path)
    
    # Save Metadata
    metadata = {
        "dataset_name": "Car Price Prediction",
        "train_shape": list(X_train_final.shape),
        "test_shape": list(X_test_final.shape),
        "numerical_features": num_cols,
        "categorical_features": cat_cols
    }
    with open(os.path.join(data_processed_dir, 'dataset_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print(f"[SUCCESS] Preprocessing pipeline completed successfully! Preprocessor saved to {preprocessor_path}.")
    print(f"[INFO] Train features: {X_train_final.shape}, Test features: {X_test_final.shape}")

if __name__ == "__main__":
    run_preprocessing()
