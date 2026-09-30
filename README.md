# MLOps Car Price Prediction Pipeline

End-to-End Enterprise MLOps Pipeline for Automobile Valuation and Regression Modeling using Scikit-Learn, MLflow Experiment Tracking, Model Registry, and Automated Champion-Challenger Lifecycle Management.

---

## 📌 Project Overview

This repository provides a modular, production-ready MLOps framework for predicting used car prices based on vehicle mechanical specifications, physical dimensions, and brand features. 

Key Highlights:
- **No Jupyter Notebook Dependency**: All EDA, preprocessing, pipeline orchestration, training, and evaluations are authored in clean, modular `.py` Python scripts.
- **Data Validation & Quality Checks**: Automated verification of input schema integrity, non-negative numerical constraints, and missing-value prevention.
- **Production Pipeline Architecture**: Sklearn `ColumnTransformer` and `Pipeline` workflows for leakage-free feature scaling, categorical one-hot encoding, and missing-value imputation.
- **Experiment Tracking with MLflow**: Comprehensive logging of hyperparameters, evaluation metrics (MAE, RMSE, R²), and serialized model artifacts.
- **Model Registry & Automated Lifecycle**: Automated stage transitions (Staging -> Production -> Archived) based on champion-challenger evaluation of $R^2$ performance metrics.

---

## 🗂️ Project Structure

```plaintext
mlops_car_price_prediction/
├── artifacts/                           # Validation and deployment metadata reports
│   ├── data_validation_report.json
│   ├── preprocessing_summary_report.json
│   ├── production_model_report.json
│   └── reproducibility_report.json
├── configs/                             # Configuration files and schemas
│   └── .gitkeep
├── data/
│   ├── raw/
│   │   └── CarPrice_Assignment.csv      # Raw source dataset
│   └── processed/                       # Cleaned, standardized, and split data
│       ├── dataset_metadata.json
│       ├── processed_dataset.csv
│       ├── train_dataset.csv
│       ├── test_dataset.csv
│       └── validation_dataset.csv
├── logs/                                # Execution and monitoring logs
│   └── .gitkeep
├── models/                              # Persisted preprocessors and trained models
│   ├── preprocessor.pkl
│   ├── random_forest_baseline.pkl
│   ├── decision_tree_baseline.pkl
│   ├── random_forest_mlflow.pkl
│   ├── scaler.pkl
│   └── ohe.pkl
├── notebooks/
│   └── project_implementation.py        # Python EDA, diagnostics & tournament runner
├── outputs/                             # Error analysis, over/under predictions, and metrics
│   ├── high_residual_errors.csv
│   ├── overpredictions.csv
│   ├── underpredictions.csv
│   ├── metrics.json
│   └── validate_outputs.py
├── pipelines/                           # Orchestration pipelines
│   ├── run_lab3_baseline.py             # Baseline pipeline (Preprocess -> Train -> Evaluate)
│   ├── run_lab4_tracking.py             # MLflow tracking & reproducibility validation
│   ├── run_lab5_pipeline.py             # Production data pipeline (Validate -> Pipeline -> Validate Outputs)
│   ├── run_lab6_registry.py             # Registry, champion-challenger lifecycle & reporting
│   ├── preprocess_pipeline.py           # Pipeline preprocessor runner
│   ├── automate_lifecycle.py           # Lifecycle automation runner
│   └── validate_reproducibility.py     # Determinism validator runner
├── reports/                             # Academic/technical documentation & registry reports
│   ├── generate_registry_report.py
│   └── Car_Price_Prediction_IEEE_Final.docx
├── src/                                 # Core source modules
│   ├── automate_lifecycle.py           # Champion-challenger model promotion
│   ├── evaluate.py                     # Evaluation metrics and error analysis
│   ├── generate_registry_report.py     # Registry deployment JSON generator
│   ├── preprocess.py                   # Baseline data transformation
│   ├── preprocess_pipeline.py          # Production Sklearn ColumnTransformer pipeline
│   ├── train.py                        # Baseline model trainer
│   ├── train_mlflow.py                 # MLflow experiment tracking
│   ├── train_registry.py               # MLflow model registry integration
│   ├── validate_data.py                # Schema & data constraint assertions
│   ├── validate_outputs.py             # Output shape and NaN assertions
│   └── validate_reproducibility.py     # Strict determinism validation
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/chandolupraneethkumar05-oss/car_price_prediction.git
   cd car_price_prediction
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux / macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Running the MLOps Pipelines

Each pipeline stage can be executed independently from the command line:

### 1. Lab 5: Production Data Pipeline
Validates raw data, fits the unified `preprocessor.pkl` ColumnTransformer, and verifies output shapes and zero-null assertions:
```bash
python pipelines/run_lab5_pipeline.py
```

### 2. Lab 3: Baseline ML Pipeline
Runs baseline feature extraction, trains Random Forest & Decision Tree baselines, and generates error analysis (`overpredictions.csv`, `underpredictions.csv`, `high_residual_errors.csv`):
```bash
python pipelines/run_lab3_baseline.py
```

### 3. Lab 4: MLflow Experiment Tracking & Reproducibility
Tracks hyperparameters and metrics in MLflow and validates 100% deterministic reproducibility across multiple runs:
```bash
python pipelines/run_lab4_tracking.py
```

### 4. Lab 6: Model Registry & Lifecycle Management
Registers candidate models in the MLflow Model Registry, attaches the preprocessor pipeline artifact, executes champion-challenger promotion to `Production`, and writes `artifacts/production_model_report.json`:
```bash
python pipelines/run_lab6_registry.py
```

### 5. Standalone EDA & Tournament Evaluation
Runs full exploratory data analysis, target distribution inspection, and multi-model benchmark tournament:
```bash
python notebooks/project_implementation.py
```

---

## 📊 Evaluation Metrics

Regression performance is tracked across multiple metrics:
- **$R^2$ Score**: Measure of variance explained by model specifications.
- **RMSE (Root Mean Squared Error)**: Standard deviation of residuals.
- **MAE (Mean Absolute Error)**: Average absolute prediction discrepancy in USD ($).

---

## 📈 MLflow UI

To view logged experiments, parameters, metrics, and registered models locally:
```bash
mlflow ui
```
Navigate to `http://localhost:5000` in your web browser.
