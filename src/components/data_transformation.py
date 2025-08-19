# Import necessary Modules
import numpy as np
import pandas as pd
from src.logger.logging_config import logging
from src.exception.exception import customexception
import os, sys
from dataclasses import dataclass
from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

from src.utils.utils import save_object


# Config class to store preprocessing pipeline path
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation(self):
        """
        Creates preprocessing pipeline for numerical and categorical features
        """
        try:
            logging.info('Data Transformation initiated')

            # Define feature groups
            categorical_cols = ['cut', 'color', 'clarity']
            numerical_cols = ['carat', 'depth', 'table', 'x', 'y', 'z']

            # Define custom category order for ordinal encoding
            cut_categories = ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            logging.info('Pipeline construction started')

            # Numerical pipeline: median imputation + standard scaling
            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])

            # Categorical pipeline: mode imputation + ordinal encoding + scaling
            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('ordinalencoder', OrdinalEncoder(
                    categories=[cut_categories, color_categories, clarity_categories])),
                ('scaler', StandardScaler())
            ])

            # Combine pipelines for numerical and categorical features
            preprocessor = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_cols),
                ('cat_pipeline', cat_pipeline, categorical_cols)
            ])

            return preprocessor

        except Exception as e:
            logging.info("Exception occurred in get_data_transformation")
            raise customexception(e, sys)

    def initialize_data_transformation(self, train_path, test_path):
        """
        Applies preprocessing to train and test datasets,
        saves the preprocessor object, and returns transformed arrays
        """
        try:
            # Load datasets
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Train and test data loaded successfully")
            logging.info(f'Train sample:\n{train_df.head().to_string()}')
            logging.info(f'Test sample:\n{test_df.head().to_string()}')

            # Get preprocessing pipeline
            preprocessing_obj = self.get_data_transformation()

            target_column_name = 'price'
            drop_columns = [target_column_name, 'id']

            # Separate input features and target
            input_feature_train_df = train_df.drop(columns=drop_columns, axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=drop_columns, axis=1)
            target_feature_test_df = test_df[target_column_name]

            # Fit-transform train set, transform test set
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info("Applied preprocessing on train and test data")

            # Concatenate input features and target for both train and test
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # Save fitted preprocessor object
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            logging.info("Preprocessing object saved as pickle")

            return (train_arr, test_arr)

        except Exception as e:
            logging.info("Exception occurred in initialize_data_transformation")
            raise customexception(e, sys)


# Commands
# python -m src.components.data_transformation