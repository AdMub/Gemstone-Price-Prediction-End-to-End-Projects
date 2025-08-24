"""
Model Evaluation Module

This script provides functionality to evaluate trained regression models using 
standard metrics (RMSE, MAE, R²). It integrates with MLflow for experiment 
tracking, logging evaluation metrics, and storing trained models. The module is 
structured around the `ModelEvaluation` class, which encapsulates metric 
calculation and MLflow logging in a clean workflow.
"""

import os
import sys
import mlflow
import mlflow.sklearn
import numpy as np
import pickle
from src.utils.utils import load_object
from urllib.parse import urlparse
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from src.logger.logging_config import logging
from src.exception.exception import customexception

class ModelEvaluation:
    """
    Handles model evaluation using standard regression metrics (RMSE, MAE, R²).
    Integrates with MLflow for experiment tracking and model logging.
    """

    def __init__(self):
        """Initialize evaluation and log the start of the process."""
        logging.info("evaluation started")

    def eval_metrics(self, actual, pred):
        """
        Compute regression evaluation metrics.
        
        Args:
            actual (array-like): Ground truth target values.
            pred (array-like): Predicted values from the model.
        
        Returns:
            tuple: (rmse, mae, r2) where
                rmse (float): Root Mean Squared Error
                mae (float): Mean Absolute Error
                r2 (float): R-squared score
        """
        rmse = np.sqrt(mean_squared_error(actual, pred))  # RMSE
        mae = mean_absolute_error(actual, pred)  # MAE
        r2 = r2_score(actual, pred)  # R²
        logging.info("evaluation metrics captured")
        return rmse, mae, r2

    def initiate_model_evaluation(self, train_array, test_array, model_path):
        """
        Run model evaluation and log metrics with MLflow.
        
        Args:
            train_array (np.ndarray): Training dataset (unused here, only test data is used).
            test_array (np.ndarray): Test dataset, last column is target, others are features.
        
        Process:
            1. Load the trained model from artifacts.
            2. Predict on test data.
            3. Evaluate using RMSE, MAE, and R².
            4. Log metrics and model into MLflow.
        """
        try:
            X_test, y_test = (test_array[:, :-1], test_array[:, -1])

            model_path = os.path.join("artifacts", "model.pkl")
            model = load_object(model_path)

            # mlflow.set_registry_uri("") #cloud usage
            
            logging.info("model has register")

            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            print(tracking_url_type_store)

            with mlflow.start_run():
                prediction = model.predict(X_test)

                (rmse, mae, r2) = self.eval_metrics(y_test, prediction)

                mlflow.log_metric("rmse", rmse)
                mlflow.log_metric("r2", r2)
                mlflow.log_metric("mae", mae)

                # Model registry does not work with file store
                if tracking_url_type_store != "file":
                    mlflow.sklearn.log_model(model, "model", registered_model_name="ml_model")
                else:
                    mlflow.sklearn.log_model(model, "model")
                
                    return {
                            "rmse": rmse,
                            "mae": mae,
                            "r2": r2
                        }
        except Exception as e:
            raise customexception(e, sys)
        
# Commands
# python -m src.components.model_evaluation
