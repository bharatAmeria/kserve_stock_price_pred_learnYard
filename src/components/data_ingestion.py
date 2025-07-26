import pandas as pd
import os
import sys
import boto3

from pandas import DataFrame
from src.logger import logging
from src.exception import MyException
from src.config import CONFIG


class IngestData:
    """
    Data ingestion class which ingests data from AWS S3 and returns a DataFrame.
    """

    def __init__(self):
        """Initialize the data ingestion class."""
        self.config = CONFIG["data_ingest"]
        logging.info("✅ IngestData class initialized with configuration.")

    def export_data_from_s3(self) -> DataFrame:
        """
        Export CSV data from AWS S3 and return it as a pandas DataFrame.
        """
        try:
            logging.info("🚀 Starting export of data from AWS S3.")

            bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
            s3_key = self.config.get("s3_data")
            feature_store_file_path = self.config.get("feature_store")

            aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
            aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

            if not all([aws_access_key, aws_secret_key, bucket_name]):
                raise ValueError("AWS credentials or bucket name missing in environment variables.")
            if not all([s3_key, feature_store_file_path]):
                raise ValueError("Missing 's3_data' or 'feature_store' in config.")

            logging.info(f"🪣 Bucket: {bucket_name}")
            logging.info(f"📄 S3 Key: {s3_key}")
            logging.info(f"📍 Destination path: {feature_store_file_path}")

            # Initialize S3 client
            s3 = boto3.client("s3",
                            region_name=aws_region,
                            aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_key)

            # Ensure local directory exists
            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)

            # Download file from S3
            s3.download_file(Bucket=bucket_name, Key=s3_key, Filename=feature_store_file_path)
            logging.info(f"✅ Downloaded S3 object to: {feature_store_file_path}")

            # Load CSV into DataFrame
            dataframe = pd.read_csv(feature_store_file_path)
            logging.info(f"📊 Loaded DataFrame with shape: {dataframe.shape}")
            return dataframe

        except Exception as e:
            logging.exception("❌ Failed to export data from AWS S3.")
            raise MyException(e, sys)


    def initiate_data_ingestion(self) -> None:
        """
        Orchestrates the data ingestion step from S3.
        """
        logging.info("🏁 Starting data ingestion process...")

        try:
            self.export_data_from_s3()
            logging.info("🎉 Data ingestion from S3 completed successfully.")
            logging.info("🏁 Exiting initiate_data_ingestion method.")

        except Exception as e:
            logging.error("❌ Data ingestion failed due to an error.")
            raise MyException(e, sys)
