import os
import sys
import joblib
import pandas as pd
from src.config import CONFIG
from src.logger import logging
from src.exception import MyException
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score,mean_squared_error

class ModelTraining:

    def __init__(self):
        """Initialize the data ingestion class."""
        self.config = CONFIG["model_training"]
        logging.info("Model training class initialized.")

    def handle_training(self, X_train, X_test, y_train, y_test) -> None:

        try:
            lr = LinearRegression()
 
            lr.fit(X_train,y_train)
            y_pred = lr.predict(X_test)

            r2_score(y_test,y_pred)
            mean_squared_error(y_test,y_pred)

            model_path = self.config["model"]
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            joblib.dump(lr,  open(model_path, 'wb'))

            return

        except Exception as e:
            logging.error("Error occurred in training", exc_info=True)
            raise MyException(e, sys)