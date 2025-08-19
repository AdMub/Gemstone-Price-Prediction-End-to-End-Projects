# ===============================
# Import Required Modules
# ===============================
import os
import sys
import pickle   # For saving/loading Python objects (e.g., trained ML models)
import numpy as np
import pandas as pd
from src.logger.logging_config import logging
from src.exception.exception import customexception
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


# ===============================
# Save Object with Pickle
# ===============================
def save_object(file_path, obj):
    """Save a Python object (e.g., trained model) to disk using pickle."""
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise customexception(e, sys)
    

# ===============================
# Train & Evaluate Multiple Models
# ===============================
def evaluate_model(X_train, y_train, X_test, y_test, models):
    """
    Train and evaluate multiple ML models.
    
    Returns:
        pd.DataFrame: A table of metrics (R², MAE, RMSE) 
                      for both training and testing sets.
    """
    try:
        records = []

        for model_name, model in models.items():
            # Train
            model.fit(X_train, y_train)

            # Predictions
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            # Training metrics
            train_r2 = r2_score(y_train, y_train_pred)
            train_mae = mean_absolute_error(y_train, y_train_pred)
            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))

            # Testing metrics
            test_r2 = r2_score(y_test, y_test_pred)
            test_mae = mean_absolute_error(y_test, y_test_pred)
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

            # Collect results
            records.append([
                model_name,
                train_r2, train_mae, train_rmse,
                test_r2, test_mae, test_rmse
            ])

        # Results DataFrame
        return pd.DataFrame(
            records,
            columns=[
                "Model",
                "Train R2", "Train MAE", "Train RMSE",
                "Test R2", "Test MAE", "Test RMSE"
            ]
        )

    except Exception as e:
        logging.info('Exception occurred during model evaluation')
        raise customexception(e, sys)
    

# ===============================
# Load Object with Pickle
# ===============================
def load_object(file_path):
    """Load a Python object (e.g., trained model) from disk using pickle."""
    try:
        with open(file_path, 'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        logging.info('Exception occurred in load_object function')
        raise customexception(e, sys)
