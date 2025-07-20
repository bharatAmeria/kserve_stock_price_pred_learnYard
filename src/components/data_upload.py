import os
import sys
import zipfile
import gdown
from dotenv import load_dotenv
from src.logger import logging
from src.exception import MyException
from src.config import CONFIG
from datetime import datetime


load_dotenv()

class UploadData:
    """
    Data ingestion class which ingests data from the source and returns a DataFrame.
    """

    def __init__(self):
        """Initialize the data ingestion class."""
        self.config = CONFIG["data_upload"]
        logging.info("Data Ingestion class initialized.")

    def download_file(self):
        """ Fetch data from the URL """
        try:
            dataset_url = self.config["source_URL"]
            zip_download_dir = self.config["local_data_file"]
            os.makedirs("artifacts/data", exist_ok=True)

            logging.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?/export=download&id='
            gdown.download(prefix + file_id, zip_download_dir)

            logging.info(f"Successfully downloaded data from {dataset_url} into file {zip_download_dir}")
        except Exception as e:
            logging.error("Error occurred while downloading file", exc_info=True)
            raise MyException(e, sys)

    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory
        """
        try:
            unzip_path = self.config["unzip_dir"]
            local_data_file = self.config["local_data_file"]

            os.makedirs(unzip_path, exist_ok=True)
            logging.info(f"Extracting zip file {local_data_file} to {unzip_path}")
            
            with zipfile.ZipFile(local_data_file, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)


            logging.info(f"Successfully extracted zip file to {unzip_path}")
        except Exception as e:
            logging.error("Error occurred while extracting zip file", exc_info=True)
            raise MyException(e, sys)
        
    def push_dataframe_to_mongodb(self, df, db_name, collection_name):
        """
        Push a pandas DataFrame to MongoDB using connection string from .env.

        Parameters:
            df (pd.DataFrame): Data to upload
            db_name (str): MongoDB database name
            collection_name (str): Collection name inside the database

        Returns:
            inserted_ids (list): List of inserted document IDs
        """
        try:
            data = df.to_dict(orient='records')
            connection_url = os.getenv("MONGODB_URI")

            if not connection_url:
                raise ValueError("MONGODB_URI not found in environment variables")

            client = pymongo.MongoClient(connection_url, tlsCAFile=certifi.where())
            database = client[db_name]
            collection = database[collection_name]
            result = collection.insert_many(data)

            mlflow.log_param("mongodb_collection", collection_name)
            mlflow.log_param("records_inserted", len(result.inserted_ids))

            return result.inserted_ids
        except Exception as e:
            mlflow.log_param("mongodb_upload_status", "failed")
            raise MyException(e, sys)
        finally:
            mlflow.end_run()
