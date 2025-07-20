import sys
import pandas as pd
from src.constants import *
from src.config import CONFIG
from src.logger import logging
from src.exception import MyException
from src.components.data_processing import DataPreprocess

class DataProcessingPipeline:
    def __init__(self):
        pass

    @staticmethod
    def main():
        config = CONFIG["data_ingest"]
        
        data = pd.read_csv(config["feature_store"])

        logging.info(">>>>>Data Preprocessing Started...<<<<<")
        data_cleaning = DataPreprocess()
        data_cleaning.handle_data(data=data)
        data_cleaning.split_data_as_train_test()
        logging.info(">>>>>Data Preprocessing Completed<<<<<\n")

        return 


if __name__ == '__main__':
    try:
        logging.info(f"*******************")
        logging.info(f">>>>>> stage {PRE_PROCESSING_STAGE_NAME} started <<<<<<")
        obj = DataProcessingPipeline()
        obj.main()
        logging.info(f">>>>>> stage {PRE_PROCESSING_STAGE_NAME} completed <<<<<<\nx==========x")
    except MyException as e:
            raise MyException(e, sys)
