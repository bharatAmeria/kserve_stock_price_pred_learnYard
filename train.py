import sys
from src.constants import *
from src.logger import logging
from src.exception import MyException
from src.pipeline.stage01_data_upload import DataUploadPipeline


try:
    logging.info(f">>>>>> stage {DATA_UPLOAD_STAGE_NAME} started <<<<<<")
    data_upload = DataUploadPipeline()
    data_upload.main()
    logging.info(f">>>>>> stage {DATA_UPLOAD_STAGE_NAME} completed <<<<<<\n\nx==========x")
except MyException as e:
    logging.exception(e, sys)
    raise e