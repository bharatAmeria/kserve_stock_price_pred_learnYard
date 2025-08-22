import kfp
from kfp import dsl
from kfp.dsl import component


BASE_IMAGE = "bharat9838/kubeflow_pipeline:latest-v3"


# ===== Upload Component =====
@component(base_image=BASE_IMAGE)
def upload_data() -> int:

    import logging
    from src.logger import logging as custom_logging  # If you have custom logger
    from src.pipeline.stage01_data_upload import DataUploadPipeline

    try:
        data_ingestion = DataUploadPipeline()
        data_ingestion.main()
        logging.info(f"✅ Uploaded {len(data_ingestion)} files to S3.")
        return len(data_ingestion)
    except Exception as e:
        logging.error(f"❌ Upload Stage failed: {e}")
        raise e

# ===== Ingestion Component =====
@component(base_image=BASE_IMAGE)
def ingest_data():

    import logging
    from src.pipeline.stage02_data_ingestion import DataIngestionPipeline
    
    try:
        logging.info("Ingestion Stage started.")
        data_processing= DataIngestionPipeline()
        data_processing.main()
        logging.info("Ingestion Stage completed.")
    except Exception as e:
        logging.error(f"Ingestion Stage failed: {e}")
        raise e

# ===== Preprocessing Component =====
@component(base_image=BASE_IMAGE)
def preprocess_data():
    
    import logging
    from src.pipeline.stage03_data_processing import DataProcessingPipeline

    try:
        logging.info("Preprocessing Stage started.")
        data_processing= DataProcessingPipeline()
        data_processing.main()
        logging.info("Preprocessing Stage completed.")
    except Exception as e:
        logging.error(f"Preprocessing Stage failed: {e}")
        raise e

# ===== Model Training Component =====
@component(base_image=BASE_IMAGE)
def train_model():
    import pandas as pd
    from src.config import CONFIG
    from src.pipeline.stage04_model_training import ModelPipeline
    from src.logger import logging

    try:
        logging.info("Model Training Stage started.")
        selection = ModelPipeline()
        selection.main()
        logging.info("Model Training Stage completed.")
    except Exception as e:
        logging.error(f"Model Training failed: {e}")
        raise e

# ===== Pipeline Definition =====
@dsl.pipeline(
    name="End-to-End ML Pipeline",
    description="Pipeline for data upload, ingestion, preprocessing, and training"
)
def ml_pipeline():
    # Define pipeline steps with proper dependencies
    step1 = upload_data()
    step2 = ingest_data().after(step1)
    step3 = preprocess_data().after(step2)
    step4 = train_model().after(step3)
    
    # Optional: Set resource requirements for components
    step1.set_memory_limit('2Gi').set_cpu_limit('1')
    step2.set_memory_limit('2Gi').set_cpu_limit('1')
    step3.set_memory_limit('4Gi').set_cpu_limit('2')
    step4.set_memory_limit('8Gi').set_cpu_limit('4')

# ===== Pipeline Compilation and Execution =====
if __name__ == "__main__":
    # Compile the pipeline
    kfp.compiler.Compiler().compile(
        pipeline_func=ml_pipeline,
        package_path='kubeflow_pipeline.yaml'
    )
    print("✅ Pipeline compiled successfully to 'kubeflow_pipeline.yaml'")