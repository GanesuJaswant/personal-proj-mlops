import os
import numpy as np
import joblib
import mlflow
import mlflow.sklearn

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def run_training():
    print("Starting MLflow Model Training for Car Price Prediction...")

    # Determine base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_processed_dir = os.path.join(base_dir, 'data', 'processed')
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)

    # 1. Load processed training and test data
    X_train_final = np.load(os.path.join(data_processed_dir, "X_train_final.npy"))
    y_train = np.load(os.path.join(data_processed_dir, "y_train.npy"))

    X_test_final = np.load(os.path.join(data_processed_dir, "X_test_final.npy"))
    y_test = np.load(os.path.join(data_processed_dir, "y_test.npy"))

    # 2. Model configuration
    n_estimators = 100
    max_depth = 10
    random_state = 42

    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state
    )

    # 3. Start MLflow experiment
    mlflow.set_experiment("Car_Price_Prediction_Tracking")

    with mlflow.start_run(run_name="RandomForest_Tracking_Run"):
        # Log parameters
        mlflow.log_param("model", "RandomForestRegressor")
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("random_state", random_state)

        # 4. Train
        model.fit(X_train_final, y_train)

        # 5. Predictions
        y_pred = model.predict(X_test_final)

        # 6. Evaluation metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = float(np.sqrt(mse))
        r2 = r2_score(y_test, y_pred)

        # 7. Log metrics
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2_score", r2)

        # 8. Save model locally
        model_path = os.path.join(models_dir, "random_forest_mlflow.pkl")
        joblib.dump(model, model_path)

        # 9. Log model to MLflow
        try:
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="random_forest_model"
            )
        except Exception:
            try:
                mlflow.sklearn.log_model(
                    sk_model=model,
                    name="random_forest_model"
                )
            except Exception:
                mlflow.sklearn.log_model(
                    sk_model=model,
                    artifact_path="random_forest_model",
                    serialization_format="cloudpickle"
                )

        print("\n[SUCCESS] MLflow run completed successfully!")
        print(f"MAE      : {mae:.2f}")
        print(f"RMSE     : {rmse:.2f}")
        print(f"R2-Score : {r2:.4f}")
        print(f"Model saved to: {model_path}\n")

if __name__ == "__main__":
    run_training()
