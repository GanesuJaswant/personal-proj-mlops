import os
import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    'symboling', 'fueltype', 'aspiration',
    'doornumber', 'carbody', 'drivewheel', 'enginelocation',
    'wheelbase', 'carlength', 'carwidth', 'carheight', 'curbweight',
    'enginetype', 'cylindernumber', 'enginesize', 'fuelsystem',
    'boreratio', 'stroke', 'compressionratio', 'horsepower',
    'peakrpm', 'citympg', 'highwaympg'
]

NUMERICAL_COLUMNS = [
    'symboling', 'wheelbase', 'carlength', 'carwidth', 'carheight',
    'curbweight', 'enginesize', 'boreratio', 'stroke', 'compressionratio',
    'horsepower', 'peakrpm', 'citympg', 'highwaympg'
]

CATEGORICAL_COLUMNS = [
    'fueltype', 'aspiration', 'doornumber', 'carbody', 'drivewheel',
    'enginelocation', 'enginetype', 'cylindernumber', 'fuelsystem'
]

def check_missing_columns(df):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    return missing

def check_negative_values(df):
    neg_cols = []
    for col in NUMERICAL_COLUMNS:
        if col in df.columns and col != 'symboling':  # symboling can be negative (-3 to 3)
            if (df[col] < 0).any():
                neg_cols.append(col)
    return neg_cols

def check_null_values(df):
    null_counts = df.isnull().sum()
    return null_counts[null_counts > 0].to_dict()
