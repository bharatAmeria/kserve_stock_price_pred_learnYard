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
    f"{project_name}/main.py",
    "app/main.py",
    "app/__init__.py",
    "app/.env",
    "app/requirements.txt",
    "app/templates/index.html",
    "app/Dockerfile",
    "kubeflow/__init__.py",
    "kubeflow/kube_flow_pipeline.py",
    ".dockerignore",
    ".env",
    ".project-root",
    "config.yaml",
    "Dockerfile",
    "InferenceService.yaml",
    "project.toml",
    "requirements.txt",
    "setup.py",
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