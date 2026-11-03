import time
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

def test_inference_latency_sla():
    # Warmup
    client.post("/predict", json=SAMPLE_CAR)

    latencies = []
    for _ in range(50):
        t0 = time.perf_counter()
        res = client.post("/predict", json=SAMPLE_CAR)
        lat = (time.perf_counter() - t0) * 1000.0
        assert res.status_code == 200
        latencies.append(lat)

    p95 = sorted(latencies)[int(len(latencies) * 0.95)]
    print(f"\n[BENCHMARK] P95 Latency: {p95:.2f}ms across 50 requests")
    assert p95 < 150.0, f"P95 latency of {p95:.2f}ms exceeded SLA threshold of 150ms"
