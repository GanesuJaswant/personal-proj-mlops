# Production Operations Runbook

## 1. Service Deployment
To deploy or update the prediction service:
```bash
# Export latest champion model
python deployment/deploy_production.py

# Build and deploy Docker container
docker build -t car-price-prediction-api:latest .
docker run -d --name car-price-api -p 8000:8000 car-price-prediction-api:latest
```

## 2. Health & Telemetry Verification
```bash
# Check service health
curl http://localhost:8000/health

# Inspect real-time inference telemetry logs
tail -n 20 logs/inference/inference_log.jsonl
```

## 3. Incident Response & Rollback
If model degradation or high prediction error is observed:
1. Revert to previous Champion version using `src/mlops_pipeline/08_automate_lifecycle.py`.
2. Inspect `artifacts/api_performance_report.json` for latency anomalies.
3. Re-run drift analysis using `python src/mlops_pipeline/12_data_drift.py`.
