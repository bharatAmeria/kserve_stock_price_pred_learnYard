from kube_flow_pipeline import ml_pipeline
from kfp import compiler
from kfp import Client

# compiler.Compiler().compile(
#     pipeline_func=ml_pipeline,
#     package_path='dev/kubeflow_pipeline.yaml'
# )

client = Client(host="http://localhost:8080")  # or public IP
pipeline = client.upload_pipeline(
    pipeline_package_path='dev/kubeflow_pipeline.yaml',
    pipeline_name='End-to-End ML Pipeline'
)

run = client.create_run_from_pipeline_package(
    pipeline_file='dev/kubeflow_pipeline.yaml',
    arguments={},
    run_name='first-run'
)
