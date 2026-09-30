import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def run_preprocessing():
    print("Starting Preprocessing Pipeline...")
    
    # Determine base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_raw_dir = os.path.join(base_dir, 'data', 'raw')
    data_processed_dir = os.path.join(base_dir, 'data', 'processed')
    models_dir = os.path.join(base_dir, 'models')
    
    os.makedirs(data_processed_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    
    # 1. Load the raw data
    data_path = os.path.join(data_raw_dir, 'CarPrice_Assignment.csv')
    if not os.path.exists(data_path):
        fallback_path = os.path.join(base_dir, 'data', 'CarPrice_Assignment.csv')
        if os.path.exists(fallback_path):
            data_path = fallback_path
            
    df = pd.read_csv(data_path)
    print(f"Loaded raw dataset with shape: {df.shape}")
    
    # 2. Data Cleaning
    # Strip whitespace from string columns
    for col in df.select_dtypes(include=['object', 'category', 'str']).columns:
        df[col] = df[col].astype(str).str.strip()
        
    # Extract car brand from CarName and standardize
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
        
    # Drop redundant ID and CarName columns
    cols_to_drop = [c for c in ['car_ID', 'CarName'] if c in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        
    # Handle missing values if any
    df = df.dropna()
    
    # Save cleaned full dataset
    df.to_csv(os.path.join(data_processed_dir, 'processed_dataset.csv'), index=False)
    
    # Separate features and target
    X = df.drop('price', axis=1)
    y = df['price']
    
    # 3. Train-Test Split (Splitting first to avoid data leakage)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Save train and test split CSVs
    train_df = df.loc[X_train.index]
    test_df = df.loc[X_test.index]
    train_df.to_csv(os.path.join(data_processed_dir, 'train_dataset.csv'), index=False)
    test_df.to_csv(os.path.join(data_processed_dir, 'test_dataset.csv'), index=False)
    test_df.to_csv(os.path.join(data_processed_dir, 'validation_dataset.csv'), index=False)
    
    # 4. Separate Column Types
    cat_cols = X_train.select_dtypes(include=['object', 'category', 'str']).columns.tolist()
    num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    # 5. Scale Numerical Features & Encode Categorical Features
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(X_train[num_cols])
    x_test_scaled = scaler.transform(X_test[num_cols])
    
    ohe = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')
    x_train_encoded = ohe.fit_transform(X_train[cat_cols])
    x_test_encoded = ohe.transform(X_test[cat_cols])
    
    # Combine Features using np.hstack
    X_train_final = np.hstack((x_train_scaled, x_train_encoded))
    X_test_final = np.hstack((x_test_scaled, x_test_encoded))
    
    # 6. Save Processed Data Arrays (.npy)
    np.save(os.path.join(data_processed_dir, 'X_train_final.npy'), X_train_final)
    np.save(os.path.join(data_processed_dir, 'X_test_final.npy'), X_test_final)
    np.save(os.path.join(data_processed_dir, 'y_train.npy'), y_train.to_numpy(dtype=np.float64))
    np.save(os.path.join(data_processed_dir, 'y_test.npy'), y_test.to_numpy(dtype=np.float64))
    
    # Save Preprocessors
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
    joblib.dump(ohe, os.path.join(models_dir, 'ohe.pkl'))
    
    # 7. Generate and Save Metadata
    metadata = {
        "dataset_name": "Car Price Prediction",
        "train_shape": list(X_train_final.shape),
        "test_shape": list(X_test_final.shape),
        "numerical_features": list(num_cols),
        "categorical_features": list(cat_cols)
    }
    with open(os.path.join(data_processed_dir, 'dataset_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print("Preprocessing completed successfully!")
    print(f"Train features shape: {X_train_final.shape}, Test features shape: {X_test_final.shape}")
    print(f"Artifacts saved in {data_processed_dir} and {models_dir}")

if __name__ == "__main__":
    run_preprocessing()
