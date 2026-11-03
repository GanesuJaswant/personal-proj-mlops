# Lab 7: Production Pipeline Architecture

## 1. Modular Stage Design
The production pipeline decomposes the MLOps lifecycle into discrete, independently executable scripts:
- `01_load_data.py`: Validates file presence and loads raw dataset.
- `02_validate_data.py`: Validates non-negative constraints and schema types.
- `03_preprocessing.py`: Executes train/test split and fits `ColumnTransformer`.
- `04_validate_outputs.py`: Verifies transformed matrix dimensions and zero nulls.
- `05_train_registry.py`: Trains candidate model and registers in MLflow.
- `06_model_evaluation.py`: Generates comprehensive error and residual reports.
- `07_quality_gate.py`: Asserts production performance thresholds.
- `08_automate_lifecycle.py`: Manages model promotion and stage transitions.

## 2. Pipeline Orchestration
Executed via `src/mlops_pipeline/churn_prediction_pipeline.py` with structured JSON execution logs saved to `logs/`.
