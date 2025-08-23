# Allow forward references for type hints (useful in modern Python typing)
from __future__ import annotations

# Standard imports
import json
from textwrap import dedent
import pendulum   # Better datetime handling (timezone-aware)

# Airflow imports
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import your custom ML training pipeline
from src.pipeline.training_pipeline import TrainingPipeline

# Initialize your ML pipeline object
training_pipeline = TrainingPipeline()

# Define an Airflow DAG (workflow)
with DAG(
    "gemstone_training_pipeline",   # Unique DAG ID (name of your workflow)
    default_args={"retries": 2},
    description="It is my training pipeline",    # Retry failed tasks 2 times
    schedule="*/5 * * * *",  # Run every 5 minutes
    # schedule="@weekly",             # Run this DAG once every week
    start_date=pendulum.datetime(2025, 8, 23, tz="UTC"),  # First execution date
    catchup=False,                  # Don't backfill old runs
    tags=["machine_learning", "classification", "gemstone"], # Metadata tags
) as dag:

    # Attach documentation to DAG (visible in Airflow UI)
    dag.doc_md = __doc__

    # ------------------ Task 1: Data Ingestion ------------------
    def data_ingestion(**kwargs):
        ti = kwargs["ti"]  # TaskInstance object, used for XCom communication
        # Run ingestion: returns paths to train and test datasets
        train_data_path, test_data_path = training_pipeline.start_data_ingestion()
        
        # Push results into Airflow XCom (for sharing across tasks)
        ti.xcom_push(
            key="data_ingestion_artifact",
            value={"train_data_path": train_data_path, "test_data_path": test_data_path},
        )

    # ------------------ Task 2: Data Transformation ------------------
    def data_transformations(**kwargs):
        import numpy as np
        ti = kwargs["ti"]
        # Pull data paths from ingestion task
        data_ingestion_artifact = ti.xcom_pull(
            task_ids="data_ingestion", key="data_ingestion_artifact"
        )
                
        # Perform preprocessing/transformation
        train_arr, test_arr = training_pipeline.start_data_transformation(
            data_ingestion_artifact["train_data_path"],
            data_ingestion_artifact["test_data_path"],
        )

        # Push results for next task
        ti.xcom_push(
            key="data_transformations_artifact",
            value={"train_arr": train_arr.tolist(), "test_arr": test_arr.tolist()},  # Convert numpy arrays to lists (so they can be stored in XCom as JSON)
        )

    # ------------------ Task 3: Model Training ------------------
    def model_trainer(**kwargs):
        import numpy as np
        ti = kwargs["ti"]
        # Pull transformed data
        data_transformation_artifact = ti.xcom_pull(
            task_ids="data_transformation",
            key="data_transformations_artifact"
        )

        # Convert lists back to numpy arrays
        train_arr = np.array(data_transformation_artifact["train_arr"])
        test_arr = np.array(data_transformation_artifact["test_arr"])

        # Train model and return path
        model_path = training_pipeline.start_model_training(train_arr, test_arr)

        # Push model artifact (so evaluation can use it)
        ti.xcom_push(
            key="model_training_artifact",
            value={"model_path": model_path}
        )

    # ------------------ Task 4: Model Evaluation ------------------
    def model_evaluation(**kwargs):
        import numpy as np
        ti = kwargs["ti"]

        # Get transformed arrays
        data_transformation_artifact = ti.xcom_pull(
            task_ids="data_transformation", 
            key="data_transformations_artifact"
        )

        # Convert lists back to numpy arrays
        train_arr = np.array(data_transformation_artifact["train_arr"])
        test_arr = np.array(data_transformation_artifact["test_arr"])

        # Get trained model path
        model_training_artifact = ti.xcom_pull(
            task_ids="model_trainer",
            key="model_training_artifact"
        )
        model_path = model_training_artifact["model_path"]

        # Run evaluation
        metrics = training_pipeline.start_model_evaluation(
            model_path=model_path, train_arr=train_arr, test_arr=test_arr
        )

        # Push metrics
        ti.xcom_push(key="evaluation_metrics", value=metrics)

    # ------------------ Task 5: Push Data to Cloud ------------------
    def push_data_to_s3(**kwargs):
        import os
        bucket_name = "repository_name"
        artifact_folder = "/app/artifacts"
        # Example: sync artifacts to S3 or Azure Blob
        # os.system(f"aws s3 sync {artifact_folder} s3://{bucket_name}/artifact")

    # ------------------ Define Operators (Tasks) ------------------
    data_ingestion_task = PythonOperator(
        task_id="data_ingestion",        # Task name
        python_callable=data_ingestion   # Function to execute
    )
    data_ingestion_task.doc_md = dedent(
        """\
        #### Ingestion task
        This task loads raw data and splits it into train/test sets.
        """
    )

    data_transform_task = PythonOperator(
        task_id="data_transformation", python_callable=data_transformations
    )
    data_transform_task.doc_md = dedent(
        """\
        #### Transformation task
        This task preprocesses the train/test data (cleaning, scaling, etc.).
        """
    )

    model_trainer_task = PythonOperator(
        task_id="model_trainer", python_callable=model_trainer
    )
    model_trainer_task.doc_md = dedent(
        """\
        #### Model Trainer Task
        This task trains the machine learning model using the transformed data.
        """
    )
    model_evaluation_task = PythonOperator(
        task_id="model_evaluation", python_callable=model_evaluation
    )
    model_evaluation_task.doc_md = dedent(
        """\
        #### Model Evaluation Task
        This task evaluates the trained machine learning model on the test data 
        and computes performance metrics (e.g., accuracy, precision, recall).
        """
    )
    push_data_to_s3_task = PythonOperator(
        task_id="push_data_to_s3", python_callable=push_data_to_s3
    )

# ------------------ Task Dependencies ------------------
# Run pipeline in order: ingestion → transformation → training → evaluating → upload
data_ingestion_task >> data_transform_task >> model_trainer_task >> model_evaluation_task >> push_data_to_s3_task
