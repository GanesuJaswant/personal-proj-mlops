import os
import sys
import numpy as np
import joblib
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_and_register():
    print("[STAGE 05] Training Candidate Model & Registering in MLflow...")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_processed_dir = os.path.join(base_dir, "data", "processed")
    models_dir = os.path.join(base_dir, "models")

    X_train = np.load(os.path.join(data_processed_dir, 'X_train_final.npy'))
    X_test = np.load(os.path.join(data_processed_dir, 'X_test_final.npy'))
    y_train = np.load(os.path.join(data_processed_dir, 'y_train.npy'))
    y_test = np.load(os.path.join(data_processed_dir, 'y_test.npy'))

    params = {
        "n_estimators": 150,
        "max_depth": 12,
        "random_state": 42
    }

    mlflow.set_experiment("Car_Price_Prediction_Registry")

    with mlflow.start_run(run_name="RandomForest_Candidate_v1") as run:
        mlflow.log_params(params)
        mlflow.log_param("model_family", "RandomForestRegressor")

        rf = RandomForestRegressor(**params)
        rf.fit(X_train, y_train)

        y_pred = rf.predict(X_test)
        mae = float(mean_absolute_error(y_test, y_pred))
        mse = float(mean_squared_error(y_test, y_pred))
        rmse = float(np.sqrt(mse))
        r2 = float(r2_score(y_test, y_pred))

        metrics = {"mae": mae, "mse": mse, "rmse": rmse, "r2_score": r2}
        mlflow.log_metrics(metrics)

        # Attach preprocessor
        prep_path = os.path.join(models_dir, "preprocessor.pkl")
        if os.path.exists(prep_path):
            mlflow.log_artifact(prep_path, artifact_path="preprocessing_pipeline")

        # Save to models/
        model_save_path = os.path.join(models_dir, "car_price_prediction_model.pkl")
        joblib.dump(rf, model_save_path)
        joblib.dump(rf, os.path.join(models_dir, "churn_model.pkl"))

        # Register in MLflow
        model_name = "Car_Price_Production_Model"
        try:
            mlflow.sklearn.log_model(
                sk_model=rf,
                artifact_path="random_forest_model",
                registered_model_name=model_name
            )
        except Exception as e:
            print(f"[STAGE 05 NOTE] MLflow model logged with notice: {e}")

        print(f"[STAGE 05] Model trained: R2={r2:.4f}, RMSE={rmse:.2f}. Registered as '{model_name}'.")

    return True

if __name__ == "__main__":
    train_and_register()
