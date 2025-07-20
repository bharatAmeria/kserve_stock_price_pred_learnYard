import os
import sys
import zipfile
import gdown
from dotenv import load_dotenv
from google.cloud import storage
from src.logger import logging
from src.exception import MyException
from src.config import CONFIG

load_dotenv()

class UploadData:
    """
    Data ingestion class which downloads data from Google Drive, extracts it,
    and uploads the contents to Google Cloud Storage.
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

    def upload_to_gcs(self):
        """
        Upload all files in extracted folder to Google Cloud Storage (GCS) bucket.
        """
        try:
            unzip_path = self.config["unzip_dir"]
            bucket_name = os.getenv("GCS_BUCKET_NAME")
            gcs_path_prefix = self.config.get("gcs_upload_prefix", "uploaded_data")

            if not bucket_name:
                raise ValueError("GCS_BUCKET_NAME not found in environment variables")

            logging.info(f"Uploading files from {unzip_path} to GCS bucket {bucket_name}")

            # Init GCS client
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)

            for root, _, files in os.walk(unzip_path):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_file_path, unzip_path)
                    blob_path = os.path.join(gcs_path_prefix, relative_path).replace("\\", "/")
                    
                    blob = bucket.blob(blob_path)
                    blob.upload_from_filename(local_file_path)

                    logging.info(f"Uploaded {local_file_path} to gs://{bucket_name}/{blob_path}")

        except Exception as e:
            logging.error("Error occurred while uploading to GCS", exc_info=True)
            raise MyException(e, sys)
