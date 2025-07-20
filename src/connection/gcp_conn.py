import os
import sys
from google.cloud import firestore
from google.oauth2 import service_account

from src.exception import MyException
from src.logger import logging
from src.constants import FIRESTORE_PROJECT_ID, FIRESTORE_CREDENTIALS_PATH

class FirestoreClient:
    """
    FirestoreClient connects to a Google Cloud Firestore database.
    
    Attributes:
    ----------
    client : firestore.Client
        A shared Firestore client instance.

    Methods:
    -------
    __init__(project_id: str)
        Initializes Firestore connection.
    """

    client = None  # Shared Firestore client

    def __init__(self, project_id: str = FIRESTORE_PROJECT_ID) -> None:
        """
        Initializes a connection to Firestore using service account credentials.

        Parameters:
        ----------
        project_id : str
            GCP project ID where Firestore is enabled.

        Raises:
        ------
        MyException
            If connection or credential loading fails.
        """
        try:
            if FirestoreClient.client is None:
                credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", FIRESTORE_CREDENTIALS_PATH)

                if not os.path.exists(credentials_path):
                    raise FileNotFoundError(f"Service account key not found at {credentials_path}")

                credentials = service_account.Credentials.from_service_account_file(credentials_path)

                FirestoreClient.client = firestore.Client(project=project_id, credentials=credentials)

                logging.info("Firestore connection initialized.")

            self.client = FirestoreClient.client
            self.project_id = project_id

        except Exception as e:
            raise MyException(e, sys)
