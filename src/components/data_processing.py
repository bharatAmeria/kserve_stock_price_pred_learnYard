import os
import sys
import numpy as np
import pandas as pd
from src.config import CONFIG
from src.logger import logging
from src.exception import MyException
from sklearn.model_selection import train_test_split

class DataPreprocess:
    """
    Data preprocessing strategy which preprocesses the data.
    """

    def __init__(self):
        """Initialize the data ingestion class."""
        self.config = CONFIG["data_ingest"]
        self.df = None
        logging.info("Data Processing class initialized.")


    def handle_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Removes columns which are not required, fills missing values with median average values,
        and converts the data type to float.
        """
        try:

            logging.info(f"Dataset shape before processing: {df.shape}")
            logging.info(f"Dataset Info before processing: {df.info()}")

            df['Date'] = pd.to_datetime(df['Date'])
            df['year'] = df['Date'].dt.year
            df['month'] = df['Date'].dt.month
            df['day'] = df['Date'].df

            df.drop('Date',axis=1,inplace=True)
            save_path = CONFIG["processed_data_path"]
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            df.to_csv(save_path, index=False)
            logging.info(f"Successfully saved processed data to {save_path}")

            self.df = df
            
            return df

        except Exception as e:
            logging.error("Error occurred in Processing data", exc_info=True)
            raise MyException(e, sys)
        
    def split_data_as_train_test(self) -> None:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
            if self.df is None:
                raise ValueError("Data must be processed first using `handle_data()` before splitting.")

            X = self.df.drop('Close', axis=1)
            y = self.df['Close']
            train_set, test_set, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")

            sclr = StandardScaler()

            X_train = sclr.fit_transform(train_set)
            X_test = sclr.transform(test_set)

            dir_path = os.path.dirname(self.config["FILE_NAME"])
            os.makedirs(dir_path,exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            os.makedirs(os.path.dirname(self.config["TRAIN_FILE_NAME"]), exist_ok=True)
            pd.DataFrame(train_set).to_csv(self.config["TRAIN_FILE_NAME"], index=False)
            pd.DataFrame(test_set).to_csv(self.config["TEST_FILE_NAME"], index=False, header=True)
            pd.DataFrame(y_train).to_csv(self.config["TRAIN_LABEL_FILE_NAME"], index=False)
            pd.DataFrame(y_test).to_csv(self.config["TEST_LABEL_FILE_NAME"], index=False)

            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise MyException(e, sys)
        