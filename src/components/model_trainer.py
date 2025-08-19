# Import Necessary modules
import numpy as np
import pandas as pd
from src.logger.logging_config import logging
from src.exception.exception import customexception
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from src.utils.utils import save_object,evaluate_model

from sklearn.linear_model import LinearRegression, Ridge,Lasso,ElasticNet
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor



@dataclass 
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')
    
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initate_model_training(self,train_array,test_array):
        try:
            logging.info('Splitting Dependent and Independent variables from train and test data')
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
            'LinearRegression':LinearRegression(),
            'Lasso':Lasso(),
            'Ridge':Ridge(),
            'Elasticnet':ElasticNet(),
            'RandomForest':RandomForestRegressor(),
            'XGboost':XGBRegressor()


        }
            
            model_report: pd.DataFrame = evaluate_model(X_train, y_train, X_test, y_test, models)
            print(model_report)
            print('\n' + '='*90 + '\n')
            logging.info(f'Model Report : \n{model_report}')

            # Get best model based on Test R2
            best_model_idx = model_report['Test R2'].idxmax()
            best_model_name = model_report.loc[best_model_idx, 'Model']
            best_model_score = model_report.loc[best_model_idx, 'Test R2']

            best_model = models[best_model_name]

            print(f"Best Model Found, Model Name: {best_model_name}, R2 Score: {best_model_score}")
            print('\n' + '='*90 + '\n')
            logging.info(f'Best Model Found , Model Name : {best_model_name} , R2 Score : {best_model_score}')

            # Save best model
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
          

        except Exception as e:
            logging.info('Exception occured at Model Training')
            raise customexception(e,sys)

# Commands
# python -m src.components.model_trainer