import os
import sys
from pandas import DataFrame
from datetime import datetime
from src.logger import logging
from src.exception import MyException
from src.config import CONFIG
from src.data_fetch.bank_churn_data import Proj1Data


class IngestData:
    """
    Data ingestion class which ingests data from the source and returns a DataFrame.
    """

    def __init__(self):
        """Initialize the data ingestion class."""
        self.config = CONFIG["data_ingest"]
        logging.info("Data Ingestion class initialized.")

     