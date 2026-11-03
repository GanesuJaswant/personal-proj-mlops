import os
import joblib
import numpy as np
import pytest
from api.preprocessing import preprocess_input

def test_model_parity_local_vs_deployment():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    deployment_model_path = os.path.join(base_dir, "deployment", "model.pkl")
    local_model_path = os.path.join(base_dir, "models", "car_price_prediction_model.pkl")
    preprocessor_path = os.path.join(base_dir, "deployment", "preprocessor.pkl")

    assert os.path.exists(deployment_model_path), "Deployment model missing"
    assert os.path.exists(local_model_path), "Local model missing"
    assert os.path.exists(preprocessor_path), "Preprocessor missing"

    dep_model = joblib.load(deployment_model_path)
    loc_model = joblib.load(local_model_path)
    prep = joblib.load(preprocessor_path)

    sample_input = {
        "symboling": 1,
        "carbrand": "toyota",
        "fueltype": "gas",
        "aspiration": "std",
        "doornumber": "four",
        "carbody": "sedan",
        "drivewheel": "fwd",
        "enginelocation": "front",
        "wheelbase": 95.7,
        "carlength": 166.3,
        "carwidth": 64.4,
        "carheight": 53.0,
        "curbweight": 2081,
        "enginetype": "ohc",
        "cylindernumber": "four",
        "enginesize": 98,
        "fuelsystem": "2bbl",
        "boreratio": 3.19,
        "stroke": 3.03,
        "compressionratio": 9.0,
        "horsepower": 70,
        "peakrpm": 4800,
        "citympg": 30,
        "highwaympg": 37
    }

    X_vec = preprocess_input(sample_input, prep)
    pred_dep = dep_model.predict(X_vec)
    pred_loc = loc_model.predict(X_vec)

    np.testing.assert_allclose(pred_dep, pred_loc, atol=1e-5, err_msg="Deployment model output diverged from local training artifact.")
