"""
prediction_pipeline.py
----------------------
This script defines the pipeline for making predictions with the trained 
machine learning model.

It includes:
1. PredictPipeline class: Handles loading the saved model and preprocessor,
   transforming incoming data, and generating predictions.
2. CustomData class: Collects user input (features like carat, depth, cut, etc.)
   and converts them into a Pandas DataFrame that can be passed into the model.

This script is used in the deployment/inference stage of the project.
"""

import os
import sys
import pandas as pd
from src.exception.exception import customexception
from src.logger.logging_config import logging
from src.utils.utils import load_object


class PredictPipeline:
    """
    Prediction pipeline class.
    Responsible for loading the trained model and preprocessor,
    applying transformations to incoming data, and generating predictions.
    """

    def __init__(self):
        print("PredictPipeline object initialized...")

    def predict(self, features):
        """
        Generate predictions for given input features.

        Args:
            features (pd.DataFrame): Input features (already structured as a DataFrame).

        Returns:
            np.ndarray: Model prediction(s).

        Raises:
            customexception: If loading or prediction fails.
        """
        try:
            # Paths to the saved preprocessor and model objects
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")
            model_path = os.path.join("artifacts", "model.pkl")

            # Load the preprocessor and model
            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)

            # Apply preprocessing (scaling, encoding, etc.) to input data
            scaled_features = preprocessor.transform(features)

            # Predict using the trained model
            predictions = model.predict(scaled_features)

            return predictions

        except Exception as e:
            raise customexception(e, sys)


class CustomData:
    """
    Custom data class for handling user input.
    Converts raw feature values into a DataFrame suitable for model prediction.
    """

    def __init__(self,
                 carat: float,
                 depth: float,
                 table: float,
                 x: float,
                 y: float,
                 z: float,
                 cut: str,
                 color: str,
                 clarity: str):
        """
        Initialize user input values.

        Args:
            carat (float): Carat weight of the gemstone.
            depth (float): Depth percentage.
            table (float): Table percentage.
            x (float): Length (mm).
            y (float): Width (mm).
            z (float): Depth (mm).
            cut (str): Cut quality (categorical).
            color (str): Color grade (categorical).
            clarity (str): Clarity grade (categorical).
        """
        self.carat = carat
        self.depth = depth
        self.table = table
        self.x = x
        self.y = y
        self.z = z
        self.cut = cut
        self.color = color
        self.clarity = clarity

    def get_data_as_dataframe(self):
        """
        Convert user input values into a Pandas DataFrame.

        Returns:
            pd.DataFrame: A single-row DataFrame with feature values.

        Raises:
            customexception: If conversion to DataFrame fails.
        """
        try:
            custom_data_input_dict = {
                'carat': [self.carat],
                'depth': [self.depth],
                'table': [self.table],
                'x': [self.x],
                'y': [self.y],
                'z': [self.z],
                'cut': [self.cut],
                'color': [self.color],
                'clarity': [self.clarity]
            }

            df = pd.DataFrame(custom_data_input_dict)
            logging.info('CustomData converted to DataFrame successfully')
            return df

        except Exception as e:
            logging.info('Exception occurred in prediction pipeline')
            raise customexception(e, sys)



# Commands
# python -m src.pipeline.prediction_pipeline