# MLflow CI Setup & Configuration

## 1. Local & CI Tracking Architecture
In CI environments (e.g. GitHub Actions), MLflow runs in headless mode using SQLite as the backend store:
```bash
export MLFLOW_TRACKING_URI="sqlite:///mlflow.db"
```

## 2. Artifact Repository
Model artifacts, parameters, metrics, and preprocessing pipelines are logged under local directory storage (`./mlruns` or relative artifact root).

## 3. Registry Operations
Model registry operations use `MlflowClient` to transition stages:
- Candidate registration -> `Stage: None`
- Quality gate validation -> `Stage: Staging`
- Champion comparison -> `Stage: Production`
