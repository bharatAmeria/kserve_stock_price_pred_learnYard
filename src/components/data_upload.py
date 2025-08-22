import os
import sys
import zipfile
import gdown
import boto3
from dotenv import load_dotenv
from src.logger import logging
from src.exception import MyException
from src.config import CONFIG

load_dotenv()

class UploadData:
    """
    Data ingestion class which downloads data from Google Drive, extracts it,
    and uploads the contents to AWS S3.
    """

    def __init__(self):
        self.config = CONFIG["data_upload"]
        logging.info("Data Ingestion class initialized.")

    def download_file(self):
        """ Download dataset ZIP file from Google Drive """
        try:
            dataset_url = os.getenv("DATASET_URI")
            zip_download_dir = self.config["local_data_file"]
            os.makedirs("artifacts/data", exist_ok=True)

            logging.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")
            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?/export=download&id='
            gdown.download(prefix + file_id, zip_download_dir)

            logging.info(f"Successfully downloaded data from {dataset_url}")
        except Exception as e:
            logging.error("Error occurred while downloading file", exc_info=True)
            raise MyException(e, sys)

    def extract_zip_file(self):
        """ Extract downloaded ZIP file """
        try:
            unzip_path = self.config["unzip_dir"]
            local_data_file = self.config["local_data_file"]

            os.makedirs(unzip_path, exist_ok=True)
            logging.info(f"Extracting zip file {local_data_file} to {unzip_path}")
            
            with zipfile.ZipFile(local_data_file, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)

            logging.info(f"Successfully extracted to {unzip_path}")
        except Exception as e:
            logging.error("Error occurred while extracting zip file", exc_info=True)
            raise MyException(e, sys)

    def upload_to_s3(self):
        """
        Upload only NFLX.csv file to AWS S3 bucket.
        """
        try:
            local_csv_path = self.config["nflx_csv_path"]
            bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
            s3_upload_prefix = self.config.get("s3_upload_prefix", "uploaded_data")

            aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
            aws_region = os.getenv("AWS_DEFAULT_REGION")

            if not aws_access_key or not aws_secret_key or not bucket_name:
                raise ValueError("AWS credentials or bucket name not found in environment variables")

            if not os.path.exists(local_csv_path):
                raise FileNotFoundError(f"NFLX.csv not found at path: {local_csv_path}")

            s3 = boto3.client("s3",
                            region_name=aws_region,
                            aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_key)

            filename = os.path.basename(local_csv_path)
            s3_key = os.path.join(s3_upload_prefix, filename).replace("\\", "/")

            s3.upload_file(local_csv_path, bucket_name, s3_key)
            logging.info(f"Uploaded {local_csv_path} to s3://{bucket_name}/{s3_key}")

            return s3_key

        except Exception as e:
            logging.error("Error occurred while uploading NFLX.csv to AWS S3", exc_info=True)
            raise MyException(e, sys)

