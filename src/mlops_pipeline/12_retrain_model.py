import os
import joblib
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

def retrain_model_v2():
    print("[STAGE 12] Retraining Model v2 on Augmented Drift Dataset...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    updated_path = os.path.join(base_dir, "data", "processed", "updated_training_data.csv")
    test_path = os.path.join(base_dir, "data", "processed", "test_dataset.csv")
    models_dir = os.path.join(base_dir, "models")

    df_train = pd.read_csv(updated_path)
    df_test = pd.read_csv(test_path)

    # Clean text columns
    for df in [df_train, df_test]:
        for col in df.select_dtypes(include=['object', 'category', 'str']).columns:
            df[col] = df[col].astype(str).str.strip()
        if 'carbrand' not in df.columns:
            if 'CarName' in df.columns:
                df['carbrand'] = df['CarName'].str.split().str[0].str.lower()
            else:
                df['carbrand'] = "toyota"
        for drop_c in ['car_ID', 'CarName']:
            if drop_c in df.columns:
                df.drop(columns=[drop_c], inplace=True)

    X_train = df_train.drop(columns=['price'], errors='ignore')
    y_train = df_train['price']
    X_test = df_test.drop(columns=['price'], errors='ignore')
    y_test = df_test['price']

    cat_cols = X_train.select_dtypes(include=['object', 'category', 'str']).columns.tolist()
    num_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()

    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('ohe', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer([
        ('num', num_pipeline, num_cols),
        ('cat', cat_pipeline, cat_cols)
    ])

    X_train_trans = preprocessor.fit_transform(X_train)
    X_test_trans = preprocessor.transform(X_test)

    rf_v2 = RandomForestRegressor(n_estimators=150, max_depth=12, random_state=42)
    rf_v2.fit(X_train_trans, y_train)

    score = r2_score(y_test, rf_v2.predict(X_test_trans))
    rmse = np.sqrt(mean_squared_error(y_test, rf_v2.predict(X_test_trans)))

    # Save retrained artifacts
    joblib.dump(rf_v2, os.path.join(models_dir, "retrained_model_v2.pkl"))
    joblib.dump(preprocessor, os.path.join(models_dir, "retrained_preprocessor_v2.pkl"))

    print(f"[STAGE 12] Retrained Model v2 Saved: Test R2={score:.4f}, RMSE={rmse:.2f}")
    return score

if __name__ == "__main__":
    retrain_model_v2()
