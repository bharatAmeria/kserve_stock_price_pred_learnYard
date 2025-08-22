import os
import sys
import boto3
import joblib
import pandas as pd
from src.config import CONFIG
from src.logger import logging
from src.exception import MyException
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score,mean_squared_error

class ModelTraining:

    def __init__(self):
        """Initialize the data ingestion class."""
        self.config = CONFIG["model_training"]
        logging.info("Model training class initialized.")

    def handle_training(self, X_train, X_test, y_train, y_test) -> None:

        try:
            # Train the model
            lr = LinearRegression()
            lr.fit(X_train, y_train)
            y_pred = lr.predict(X_test)

            r2 = r2_score(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            logging.info(f"Model evaluation: R2={r2}, MSE={mse}")

            # Save model locally (temporary)
            local_model_path = self.config["model"]
            os.makedirs("artifacts/trained_model", exist_ok=True)
            joblib.dump(lr, open(local_model_path, "wb"))

            # AWS details
            bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
            s3_upload_prefix = self.config.get("s3_upload_prefix", "models")

            aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
            aws_region = os.getenv("AWS_DEFAULT_REGION")

            if not aws_access_key or not aws_secret_key or not bucket_name:
                raise ValueError("AWS credentials or bucket name not found in environment variables")

            # Initialize S3 client
            s3 = boto3.client(
                "s3",
                region_name=aws_region,
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key
            )

            # Define S3 path
            filename = os.path.basename(local_model_path)
            s3_key = os.path.join(s3_upload_prefix, filename).replace("\\", "/")

            # Upload model to S3
            s3.upload_file(local_model_path, bucket_name, s3_key)
            logging.info(f"Uploaded model to s3://{bucket_name}/{s3_key}")

            # Optionally remove local copy
            if os.path.exists(local_model_path):
                os.remove(local_model_path)

            return s3_key

        except Exception as e:
            logging.error("Error occurred while saving model to AWS S3", exc_info=True)
            raise MyException(e, sys)