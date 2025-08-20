import kfp
from kfp import dsl
from src.logger import logging
from kfp.dsl import component
from src.pipeline.stage01_data_upload import DataUploadPipeline
from src.pipeline.stage02_data_ingestion import DataIngestionPipeline
from src.pipeline.stage03_data_processing import DataProcessingPipeline
from src.pipeline.stage04_model_training import ModelPipeline


BASE_IMAGE = "kfp-local:latest"


# ===== Upload Component =====
@component(base_image=BASE_IMAGE)
def upload_data() -> int:

    try:
        data_ingestion = DataUploadPipeline()
        data_ingestion.main()
        logging.info(f"✅ Uploaded {len(data_ingestion)} files to S3.")
        return len(data_ingestion)
    except Exception as e:
        logging.error(f"❌ Upload Stage failed: {e}")
        raise e

# ===== Ingestion Component =====
@component(base_image=BASE_IMAGE)
def ingest_data():
    try:
        logging.info("Ingestion Stage started.")
        data_processing= DataIngestionPipeline()
        data_processing.main()
        logging.info("Ingestion Stage completed.")
    except Exception as e:
        logging.error(f"Ingestion Stage failed: {e}")
        raise e

# ===== Preprocessing Component =====
@component(base_image=BASE_IMAGE)
def preprocess_data():

    try:
        logging.info("Preprocessing Stage started.")
        data_processing= DataProcessingPipeline()
        data_processing.main()
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
        logging.info("Model Training Stage started.")
        selection = ModelPipeline()
        selection.main()
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
