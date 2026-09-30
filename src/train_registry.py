import os
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_and_register_model():
    print("[INFO] --- Starting MLflow Run with Model Registry for Car Price Prediction ---")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_processed_dir = os.path.join(base_dir, 'data', 'processed')
    models_dir = os.path.join(base_dir, 'models')
    
    # 1. Set up MLflow
    mlflow.set_experiment("Car_Price_Prediction_Registry")
    
    # 2. Load Processed Data
    try:
        X_train = np.load(os.path.join(data_processed_dir, 'X_train_final.npy'))
        X_test = np.load(os.path.join(data_processed_dir, 'X_test_final.npy'))
        y_train = np.load(os.path.join(data_processed_dir, 'y_train.npy'))
        y_test = np.load(os.path.join(data_processed_dir, 'y_test.npy'))
    except FileNotFoundError:
        print("[ERROR] Processed data not found. Please run the preprocessing pipeline first.")
        return
    
    # 3. Define Model Parameters
    params = {
        "n_estimators": 150,
        "max_depth": 12,
        "random_state": 42
    }
    
    with mlflow.start_run(run_name="RandomForest_Registry_Candidate") as run:
        # Log parameters
        mlflow.log_params(params)
        mlflow.log_param("model_family", "RandomForestRegressor")
        
        # 4. Train Model
        print("[INFO] Training RandomForestRegressor model...")
        rf_model = RandomForestRegressor(**params)
        rf_model.fit(X_train, y_train)
        
        # 5. Evaluate
        print("[INFO] Evaluating model...")
        y_pred = rf_model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = float(np.sqrt(mse))
        r2 = r2_score(y_test, y_pred)
        
        metrics = {
            "mae": mae,
            "mse": mse,
            "rmse": rmse,
            "r2_score": r2
        }
        mlflow.log_metrics(metrics)
        
        # 6. LOG PREPROCESSOR PIPELINE (Lineage)
        preprocessor_path = os.path.join(models_dir, "preprocessor.pkl")
        if os.path.exists(preprocessor_path):
            print("[INFO] Attaching preprocessing pipeline to model artifacts...")
            mlflow.log_artifact(preprocessor_path, artifact_path="preprocessing_pipeline")
        else:
            print("[WARNING] models/preprocessor.pkl not found, skipping preprocessor artifact attachment.")
            
        # 7. LOG AND REGISTER THE MODEL
        registered_model_name = "Car_Price_Production_Model"
        print(f"[INFO] Pushing model to MLflow Registry as '{registered_model_name}'...")
        try:
            mlflow.sklearn.log_model(
                sk_model=rf_model,
                artifact_path="random_forest_model",
                registered_model_name=registered_model_name
            )
        except Exception:
            try:
                mlflow.sklearn.log_model(
                    sk_model=rf_model,
                    name="random_forest_model",
                    registered_model_name=registered_model_name
                )
            except Exception:
                mlflow.sklearn.log_model(
                    sk_model=rf_model,
                    artifact_path="random_forest_model",
                    registered_model_name=registered_model_name,
                    serialization_format="cloudpickle"
                )
        
        print(f"[SUCCESS] Metrics logged: R2 = {r2:.4f} | RMSE = {rmse:.2f} | MAE = {mae:.2f}")
        print(f"[SUCCESS] Model successfully registered under name: '{registered_model_name}'")

if __name__ == "__main__":
    train_and_register_model()
