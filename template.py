import os
from pathlib import Path

project_name = "src"

list_of_files = [

    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_processing.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_upload.py",
    f"{project_name}/components/model.py",
    f"{project_name}/config/__init__.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/stage01_data_upload.py",
    f"{project_name}/pipeline/stage02_data_ingestion.py",
    f"{project_name}/pipeline/stage03_data_processing.py",
    f"{project_name}/pipeline/stage04_model_training.py",
    "app/app.py",
    "app/requirements.txt",
    "app/template/index.html",
    "app/Dockerfile",
    "dev/deployment.yaml",
    "dev/InferenceService.yaml",
    "kubeflow/kube_flow_pipeline.py",
    "kubeflow/ml_pipe.py",
    "train.py",
    "requirements.txt",
    "setup.py",
    "project.toml",
    "config.yaml",
    "Dockerfile",
    "testEnvironment.py",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        print(f"file is already present at: {filepath}")