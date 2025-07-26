import sys
import pandas as pd
from src.constants import *
from src.components.data_upload import UploadData
from src.logger import logging
from src.exception import MyException

class DataUploadPipeline:
    def __init__(self):
        pass

    @staticmethod
    def main():
        upload = UploadData()
        upload.download_file()
        upload.extract_zip_file()
        upload.upload_to_s3()



if __name__ == '__main__':
    try:
        logging.info(f">>>>>> stage {INGESTION_STAGE_NAME} started <<<<<<")
        obj = DataUploadPipeline()
        obj.main()
    except MyException as e:
            raise MyException(e, sys)