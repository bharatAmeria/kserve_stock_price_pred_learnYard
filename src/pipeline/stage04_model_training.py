import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import MyException
from src.components.model import ModelTraining
from src.config import CONFIG
class ModelPipeline:
    def __init__(self):
        pass

    @staticmethod
    def main():
        
        config = CONFIG["model_training"]
        X_train = pd.read_csv(config["TRAIN_FILE_NAME"])
        X_test = pd.read_csv(config["TEST_FILE_NAME"])
        y_train = pd.read_csv(config["TRAIN_LABEL_FILE_NAME"])
        y_test = pd.read_csv(config["TEST_LABEL_FILE_NAME"])

        logging.info(">>>>>Model Training Started...<<<<<")
        train = ModelTraining()
        train.handle_training(X_train, X_test, y_train, y_test)
        logging.info(">>>>>Model Training Completed<<<<<\n")

        return 
    
if __name__ == '__main__':
    try:
        logging.info(f"*******************")
        logging.info(f">>>>>> stage started <<<<<<")
        obj = ModelPipeline()
        obj.main()
        logging.info(f">>>>>> stage completed <<<<<<\nx==========x")
    except MyException as e:
            raise MyException(e, sys)
    