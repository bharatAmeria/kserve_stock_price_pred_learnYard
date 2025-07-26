import sys
from src.constants import *
from src.logger import logging
from src.exception import MyException
from src.pipeline.stage01_data_upload import DataUploadPipeline
from src.pipeline.stage02_data_ingestion import DataIngestionPipeline
from src.pipeline.stage03_data_processing import DataProcessingPipeline
from src.pipeline.stage04_model_training import ModelPipeline

try:
    logging.info(f">>>>>> stage {DATA_UPLOAD_STAGE_NAME} started <<<<<<")
    data_ingestion = DataUploadPipeline()
    data_ingestion.main()
    logging.info(f">>>>>> stage {DATA_UPLOAD_STAGE_NAME} completed <<<<<<\n\nx==========x")
except MyException as e:
    logging.exception(e, sys)
    raise e

try:
    logging.info(f">>>>>> stage {INGESTION_STAGE_NAME} started <<<<<<")
    data_processing= DataIngestionPipeline()
    data_processing.main()
    logging.info(f">>>>>> stage {INGESTION_STAGE_NAME} completed <<<<<<\n\nx==========x")
except MyException as e:
    logging.exception(e, sys)
    raise e

try:
    logging.info(f">>>>>> stage {PRE_PROCESSING_STAGE_NAME} started <<<<<<")
    data_processing= DataProcessingPipeline()
    data_processing.main()
    logging.info(f">>>>>> stage {PRE_PROCESSING_STAGE_NAME} completed <<<<<<\n\nx==========x")
except MyException as e:
    logging.exception(e, sys)
    raise e

try:
    logging.info(f">>>>>> stage Model training started <<<<<<")
    selection = ModelPipeline()
    selection.main()
    logging.info(f">>>>>> stage Model training completed <<<<<<\n\nx==========x")
except MyException as e:
    logging.exception(e, sys)
    raise e