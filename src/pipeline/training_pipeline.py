"""
training_pipeline.py

End-to-End ML pipeline for Diamond Price Prediction.

Steps:
1. Data Ingestion      - Reads raw data and prepares train/test datasets.
2. Data Transformation - Cleans, preprocesses, and encodes the data.
3. Model Training      - Trains regression models.
4. Model Evaluation    - Evaluates models with R², MAE, RMSE metrics.

Ensures a structured ML lifecycle with reproducibility.
"""

import sys
from src.logger.logging_config import logging
from src.exception.exception import customexception

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation


class TrainingPipeline:
    def start_data_ingestion(self):
        try:
            logging.info("Step 1: Data Ingestion started...")
            data_ingestion = DataIngestion()
            train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed. Train: {train_data_path}, Test: {test_data_path}")
            return train_data_path, test_data_path
        except Exception as e:
            raise customexception(e, sys)
        
    def start_data_transformation(self, train_data_path, test_data_path):
        try:
            logging.info("Step 2: Data Transformation started...")
            data_transformation = DataTransformation()
            train_arr, test_arr = data_transformation.initialize_data_transformation(
                train_data_path, test_data_path
            )
            logging.info("Data Transformation completed. Features scaled & encoded.")
            return train_arr, test_arr
        except Exception as e:
            raise customexception(e, sys)
    
    def start_model_training(self, train_arr, test_arr):
        try:
            logging.info("Step 3: Model Training started...")
            model_trainer = ModelTrainer()
            model_path = model_trainer.initate_model_training(train_arr, test_arr)
            logging.info(f"Model Training completed. Model saved at: {model_path}")
            return model_path
        except Exception as e:
            raise customexception(e, sys)
    
    def start_model_evaluation(self, train_arr, test_arr, model_path):
        try:
            logging.info("Step 4: Model Evaluation started...")
            model_eval = ModelEvaluation()
            metrics = model_eval.initiate_model_evaluation(train_arr, test_arr, model_path)
            logging.info(f"Model Evaluation completed. Metrics: {metrics}")
            return metrics
        except Exception as e:
            raise customexception(e, sys)

    def start_training(self):
        try:
            logging.info("==== Training Pipeline Started ====")
            
            # Step 1 & 2: Data ingestion + transformation
            train_data_path, test_data_path = self.start_data_ingestion()
            train_arr, test_arr = self.start_data_transformation(train_data_path, test_data_path)

            # Step 3: Training
            model_path = self.start_model_training(train_arr, test_arr)

            # Step 4: Evaluation
            metrics = self.start_model_evaluation(train_arr, test_arr, model_path)

            logging.info("==== Training Pipeline Completed Successfully ====")
            return metrics
        except Exception as e:
            logging.error("Error occurred during training pipeline execution.")
            raise customexception(e, sys)


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    results = pipeline.start_training()
    print("Final Evaluation Metrics:", results)



# Commands
# python -m src.pipeline.training_pipeline
