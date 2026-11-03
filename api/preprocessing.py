import pandas as pd
import numpy as np

BRAND_CORRECTIONS = {
    "maxda": "mazda",
    "porcshce": "porsche",
    "toyouta": "toyota",
    "vokswagen": "volkswagen",
    "vw": "volkswagen"
}

def preprocess_input(data_dict, preprocessor):
    df = pd.DataFrame([data_dict])
    
    # Clean text columns
    for col in df.select_dtypes(include=['object', 'category', 'str']).columns:
        df[col] = df[col].astype(str).str.strip()

    # Determine carbrand
    if 'carbrand' not in df.columns or df['carbrand'].iloc[0] is None:
        if 'CarName' in df.columns and df['CarName'].iloc[0]:
            df['carbrand'] = df['CarName'].str.split().str[0].str.lower()
        else:
            df['carbrand'] = "toyota"

    df['carbrand'] = df['carbrand'].astype(str).str.lower().replace(BRAND_CORRECTIONS)

    # Drop non-feature columns if present
    for drop_col in ['car_ID', 'CarName', 'price']:
        if drop_col in df.columns:
            df = df.drop(columns=[drop_col])

    # Transform using serialized ColumnTransformer
    X_processed = preprocessor.transform(df)
    return X_processed

def preprocess_batch(data_dicts, preprocessor):
    df = pd.DataFrame(data_dicts)
    for col in df.select_dtypes(include=['object', 'category', 'str']).columns:
        df[col] = df[col].astype(str).str.strip()

    if 'carbrand' not in df.columns or df['carbrand'].isnull().all():
        if 'CarName' in df.columns:
            df['carbrand'] = df['CarName'].str.split().str[0].str.lower()
        else:
            df['carbrand'] = "toyota"
    else:
        df['carbrand'] = df['carbrand'].fillna("toyota")

    df['carbrand'] = df['carbrand'].astype(str).str.lower().replace(BRAND_CORRECTIONS)

    for drop_col in ['car_ID', 'CarName', 'price']:
        if drop_col in df.columns:
            df = df.drop(columns=[drop_col])

    return preprocessor.transform(df)
