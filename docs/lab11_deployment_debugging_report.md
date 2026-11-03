# Lab 11: Deployment Debugging & Troubleshooting Report

## 1. Identified Challenges & Resolutions
1. **Missing Directory for Inference Logs**:
   - *Symptom*: Container crashed upon receiving first `/predict` request due to missing `logs/inference/` path.
   - *Fix*: Created the directory during Docker image build and assigned ownership to `appuser`.

2. **Model Deserialization Mismatch**:
   - *Symptom*: `ModuleNotFoundError` during `joblib.load` when relative paths were improperly resolved.
   - *Fix*: Centralized artifact path resolution via `get_base_dir()` in `api/model_loader.py`.

3. **Kubernetes Readiness Probe Flapping**:
   - *Symptom*: Pod reported Unready during model warm-up.
   - *Fix*: Configured `initialDelaySeconds: 5` and `periodSeconds: 5` for readiness probe.
