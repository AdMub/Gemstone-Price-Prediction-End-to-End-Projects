# Import necessary modules
import numpy as np
import pandas as pd
from src.logger.logging_config import logging
from src.exception.exception import customexception

import os
import sys
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from pathlib import Path


# Config Class (holds file paths for where data will be stored)
@dataclass   # automatically gives this class an __init__ method
class DataIngestionConfig:
    raw_data_path:str=os.path.join("artifacts","raw.csv")
    train_data_path:str=os.path.join("artifacts","train.csv")
    test_data_path:str=os.path.join("artifacts","test.csv")

# DataIngestion Class (loads the config with those file paths)
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
        

    # Ingestion Method
    def initiate_data_ingestion(self):
        logging.info("data ingestion started")
        try:
            data=pd.read_csv("experiment/datasets/train.csv")
            logging.info(" reading a df")

            # Saving Raw Data
            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.raw_data_path)),exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path,index=False)
            logging.info(" i have saved the raw dataset in artifact folder")
            
            # Train-Test Split
            logging.info("here i have performed train test split")

            train_data,test_data=train_test_split(data,test_size=0.25)
            logging.info("train test split completed")
            
            train_data.to_csv(self.ingestion_config.train_data_path,index=False)
            test_data.to_csv(self.ingestion_config.test_data_path,index=False)
            
            logging.info("data ingestion part completed")
            
            # Returning Paths
            return (
                 
                
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )



        # Exception Handling
        except Exception as e:
            logging.info()
            raise customexception(e,sys)


# Running the Script
if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()
    logging.info("✅ Data ingestion completed successfully!")



# Commands
# python -m src.components.data_ingestion
