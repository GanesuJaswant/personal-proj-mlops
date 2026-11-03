import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

SAMPLE_CAR = {
    "symboling": 3,
    "carbrand": "alfa-romero",
    "fueltype": "gas",
    "aspiration": "std",
    "doornumber": "two",
    "carbody": "convertible",
    "drivewheel": "rwd",
    "enginelocation": "front",
    "wheelbase": 88.6,
    "carlength": 168.8,
    "carwidth": 64.1,
    "carheight": 48.8,
    "curbweight": 2548,
    "enginetype": "dohc",
    "cylindernumber": "four",
    "enginesize": 130,
    "fuelsystem": "mpfi",
    "boreratio": 3.47,
    "stroke": 2.68,
    "compressionratio": 9.0,
    "horsepower": 111,
    "peakrpm": 5000,
    "citympg": 21,
    "highwaympg": 27
}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "telemetry_destination" in data

def test_predict_valid():
    response = client.post("/predict", json=SAMPLE_CAR)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["predicted_price"] > 0
    assert "inference_id" in data

def test_predict_with_carname():
    car = SAMPLE_CAR.copy()
    car.pop("carbrand", None)
    car["CarName"] = "toyota corolla"
    response = client.post("/predict", json=car)
    assert response.status_code == 200
    assert response.json()["predicted_price"] > 0

def test_batch_predict():
    payload = {"records": [SAMPLE_CAR, SAMPLE_CAR]}
    response = client.post("/batch-predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["predictions"]) == 2

def test_predict_invalid_schema():
    response = client.post("/predict", json={"symboling": "not-an-int"})
    assert response.status_code == 422
