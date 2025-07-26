import kfp
from kfp import dsl
from kfp.dsl import component

# Change this to your actual ACR image path
BASE_IMAGE = "myacr123.azurecr.io/ml-pipeline:latest"

# ===== Upload Component =====
@component(base_image=BASE_IMAGE)
def upload_data() -> int:
    from src.components.data_upload import UploadData
    from src.logger import logging

    try:
        upload = UploadData()
        upload.download_file()
        upload.extract_zip_file()
        inserted = upload.upload_to_azure_blob()
        logging.info(f"{len(inserted)} documents inserted.")
        return len(inserted)
    except Exception as e:
        logging.error(f"Upload Stage failed: {e}")
        raise e

# ===== Ingestion Component =====
@component(base_image=BASE_IMAGE)
def ingest_data():
    from src.components.data_ingestion import IngestData
    from src.logger import logging

    try:
        logging.info("Ingestion Stage started.")
        ingestor = IngestData()
        ingestor.initiate_data_ingestion()
        logging.info("Ingestion Stage completed.")
    except Exception as e:
        logging.error(f"Ingestion Stage failed: {e}")
        raise e

# ===== Preprocessing Component =====
@component(base_image=BASE_IMAGE)
def preprocess_data():
    import pandas as pd
    from src.config import CONFIG
    from src.components.data_processing import DataPreprocess
    from src.logger import logging

    try:
        config = CONFIG["data_ingest"]
        data = pd.read_csv(config["feature_store"])

        logging.info("Preprocessing Stage started.")
        cleaner = DataPreprocess()
        cleaner.handle_data(data=data)
        cleaner.split_data_as_train_test()
        logging.info("Preprocessing Stage completed.")
    except Exception as e:
        logging.error(f"Preprocessing Stage failed: {e}")
        raise e

# ===== Model Training Component =====
@component(base_image=BASE_IMAGE)
def train_model():
    import pandas as pd
    from src.config import CONFIG
    from src.components.model import ModelTraining
    from src.logger import logging

    try:
        config = CONFIG["model_training"]
        X_train = pd.read_csv(config["TRAIN_FILE_NAME"])
        X_test = pd.read_csv(config["TEST_FILE_NAME"])
        y_train = pd.read_csv(config["TRAIN_LABEL_FILE_NAME"])
        y_test = pd.read_csv(config["TEST_LABEL_FILE_NAME"])

        logging.info("Model Training Stage started.")
        trainer = ModelTraining()
        trainer.handle_training(X_train, X_test, y_train, y_test)
        logging.info("Model Training Stage completed.")
    except Exception as e:
        logging.error(f"Model Training failed: {e}")
        raise e

# ===== Pipeline Definition =====
@dsl.pipeline(
    name="End-to-End ML Pipeline",
    description="Pipeline for data upload, ingestion, preprocessing, and training"
)
def ml_pipeline():
    step1 = upload_data()
    step2 = ingest_data().after(step1)
    step3 = preprocess_data().after(step2)
    step4 = train_model().after(step3)
