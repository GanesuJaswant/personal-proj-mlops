import os
import sys
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
    print("[STAGE 03] Executing Feature Preprocessing & Pipeline Construction...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_raw_path = os.path.join(base_dir, "data", "raw", "CarPrice_Assignment.csv")
    data_processed_dir = os.path.join(base_dir, "data", "processed")
    models_dir = os.path.join(base_dir, "models")
    artifacts_dir = os.path.join(base_dir, "artifacts")

    os.makedirs(data_processed_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(artifacts_dir, exist_ok=True)

    if not os.path.exists(data_raw_path):
        data_raw_path = os.path.join(base_dir, "data", "raw", "churn.csv")

    df = pd.read_csv(data_raw_path)

    # Clean text columns
    for col in df.select_dtypes(include=['object', 'category', 'str']).columns:
        df[col] = df[col].astype(str).str.strip()

    # Brand extraction
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

    X = df.drop('price', axis=1)
    y = df['price']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    cat_cols = X_train.select_dtypes(include=['object', 'category', 'str']).columns.tolist()
    num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()

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

    X_train_final = preprocessor.fit_transform(X_train)
    X_test_final = preprocessor.transform(X_test)

    # Save processed arrays
    np.save(os.path.join(data_processed_dir, 'X_train_final.npy'), X_train_final)
    np.save(os.path.join(data_processed_dir, 'X_test_final.npy'), X_test_final)
    np.save(os.path.join(data_processed_dir, 'y_train.npy'), y_train.to_numpy(dtype=np.float64))
    np.save(os.path.join(data_processed_dir, 'y_test.npy'), y_test.to_numpy(dtype=np.float64))

    # Save preprocessor artifact
    preprocessor_path = os.path.join(models_dir, 'preprocessor.pkl')
    joblib.dump(preprocessor, preprocessor_path)

    # Save summary report
    summary = {
        "status": "SUCCESS",
        "raw_shape": list(df.shape),
        "train_features_shape": list(X_train_final.shape),
        "test_features_shape": list(X_test_final.shape),
        "numerical_columns": num_cols,
        "categorical_columns": cat_cols,
        "preprocessor_saved": preprocessor_path
    }
    with open(os.path.join(artifacts_dir, 'preprocessing_summary_report.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=4)

    print(f"[STAGE 03] Preprocessing complete. Transformed features: {X_train_final.shape[1]}. Saved to {preprocessor_path}.")
    return True

if __name__ == "__main__":
    run_preprocessing()
