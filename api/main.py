import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import (
    CarFeaturesInput,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    HealthResponse
)
from api.model_loader import load_artifacts
from api.preprocessing import preprocess_input, preprocess_batch
from api.monitoring_logger import log_inference

MODEL = None
PREPROCESSOR = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global MODEL, PREPROCESSOR
    try:
        MODEL, PREPROCESSOR = load_artifacts()
        print("[INFO] Model and preprocessor loaded successfully during startup.")
    except Exception as e:
        print(f"[WARNING] Startup artifact loading failed: {e}")
    yield

app = FastAPI(
    title="Car Price Prediction MLOps Service",
    description="Production-grade REST API serving automobile price regression predictions with continuous telemetry logging.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "service": "Car Price Prediction API",
        "version": "1.0.0",
        "endpoints": ["/health", "/predict", "/batch-predict", "/metrics"]
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health():
    global MODEL, PREPROCESSOR
    if MODEL is None or PREPROCESSOR is None:
        try:
            MODEL, PREPROCESSOR = load_artifacts()
        except Exception:
            pass
    loaded = MODEL is not None and PREPROCESSOR is not None
    return HealthResponse(
        status="healthy" if loaded else "degraded",
        service="Car Price Prediction Service",
        model_loaded=loaded,
        version="1.0.0"
    )

@app.post("/predict", response_model=PredictionResponse, tags=["Inference"])
def predict(payload: CarFeaturesInput):
    global MODEL, PREPROCESSOR
    if MODEL is None or PREPROCESSOR is None:
        MODEL, PREPROCESSOR = load_artifacts()

    start_time = time.time()
    inference_id = str(uuid.uuid4())

    try:
        input_data = payload.model_dump()
        X_vec = preprocess_input(input_data, PREPROCESSOR)
        pred_value = float(MODEL.predict(X_vec)[0])
        latency_ms = (time.time() - start_time) * 1000.0

        # Log for continuous monitoring
        log_inference(inference_id, input_data, pred_value, latency_ms)

        return PredictionResponse(
            status="success",
            predicted_price=round(pred_value, 2),
            currency="USD",
            model_version="Production_Champion_v1",
            inference_id=inference_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@app.post("/batch-predict", response_model=BatchPredictionResponse, tags=["Inference"])
def batch_predict(payload: BatchPredictionRequest):
    global MODEL, PREPROCESSOR
    if MODEL is None or PREPROCESSOR is None:
        MODEL, PREPROCESSOR = load_artifacts()

    try:
        data_list = [r.model_dump() for r in payload.records]
        X_mat = preprocess_batch(data_list, PREPROCESSOR)
        preds = MODEL.predict(X_mat).tolist()
        rounded_preds = [round(float(p), 2) for p in preds]

        return BatchPredictionResponse(
            status="success",
            count=len(rounded_preds),
            predictions=rounded_preds,
            model_version="Production_Champion_v1"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch inference error: {str(e)}")

@app.get("/metrics", tags=["Monitoring"])
def metrics():
    return {
        "model_type": type(MODEL).__name__ if MODEL else "None",
        "service_uptime": "stable",
        "telemetry_destination": "logs/inference/inference_log.jsonl"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
