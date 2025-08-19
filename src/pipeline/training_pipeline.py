"""
training_pipeline.py

This script orchestrates the end-to-end machine learning workflow for 
diamond price prediction. It ties together all components of the pipeline:

1. Data Ingestion     - Reads raw data and prepares training/test datasets.
2. Data Transformation - Cleans, preprocesses, and encodes the data.
3. Model Training     - Trains regression models using the processed data.
4. Model Evaluation   - Evaluates trained models with R², MAE, and RMSE metrics.

The script ensures a structured ML lifecycle and enables reproducibility
for experiments and production deployment.
"""

import os
import sys
from src.logger.logging_config import logging
from src.exception.exception import customexception
import pandas as pd

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation


if __name__ == "__main__":
    try:
        logging.info("==== Training Pipeline Started ====")

        # Step 1: Data Ingestion
        logging.info("Step 1: Data Ingestion started...")
        obj = DataIngestion()
        train_data_path, test_data_path = obj.initiate_data_ingestion()
        logging.info(f"Data Ingestion completed. Train path: {train_data_path}, Test path: {test_data_path}")

        # Step 2: Data Transformation
        logging.info("Step 2: Data Transformation started...")
        data_transformation = DataTransformation()
        train_arr, test_arr = data_transformation.initialize_data_transformation(
            train_data_path, test_data_path
        )
        logging.info("Data Transformation completed. Features scaled & encoded.")

        # Step 3: Model Training
        logging.info("Step 3: Model Training started...")
        model_trainer_obj = ModelTrainer()
        model_trainer_obj.initate_model_training(train_arr, test_arr)
        logging.info("Model Training completed successfully.")

        # Step 4: Model Evaluation
        logging.info("Step 4: Model Evaluation started...")
        model_eval_obj = ModelEvaluation()
        model_eval_obj.initiate_model_evaluation(train_arr, test_arr)
        logging.info("Model Evaluation completed. Metrics logged.")

        logging.info("==== Training Pipeline Completed Successfully ====")

    except Exception as e:
        logging.error("Error occurred during training pipeline execution.")
        raise customexception(e, sys)

# Commands
# python -m src.pipeline.training_pipeline