from pathlib import Path

CONFIG_FILE_PATH = Path("config/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")

# For MongoDB connection
DATABASE_NAME = "Churn_rate" 
COLLECTION_NAME = "Churn_Data"
MONGODB_URL_KEY = "MONGODB_URL"

"""
---------------------------------------------------------------
Training Pipeline related constant start with DATA_INGESTION VAR NAME
---------------------------------------------------------------
"""
PIPELINE_NAME: str = ""
ARTIFACT_DIR: str = "artifact"
TRAINING_STAGE_NAME = "Training Pipeline"

"""
---------------------------------------------------------------
Environment Test and Dependency related constant 
---------------------------------------------------------------
"""
REQUIRED_PYTHON = "python3"
REQUIREMENTS_FILE = "requirements.txt"

"""
---------------------------------------------------------------
Data ingestion related constant 
---------------------------------------------------------------
"""
INGESTION_STAGE_NAME = "Data Ingestion"
DATA_UPLOAD_STAGE_NAME = "Data Upload"
"""
---------------------------------------------------------------
Data PrePrecessing related constant 
---------------------------------------------------------------
"""
PRE_PROCESSING_STAGE_NAME = "Data Pre-Processing"


"""
---------------------------------------------------------------
FEATURE Selection related constant 
---------------------------------------------------------------
"""
FEATURE_SELECTION_STAGE = "Feature Selection"

"""
---------------------------------------------------------------
Model Selection related constant 
---------------------------------------------------------------
"""

REQUIRED_PYTHON = "python3"
REQUIREMENTS_FILE = "requirements.txt"