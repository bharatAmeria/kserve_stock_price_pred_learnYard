from kfp import compiler, Client
from kube_flow_pipeline import ml_pipeline

# ========== CONFIG ==========
PIPELINE_NAME = "end-to-end-ml-pipeline"
EXPERIMENT_NAME = "ml-experiment"
RUN_NAME = "ml-pipeline-first-run"
PIPELINE_FILE = "kubeflow_pipeline.yaml"
KFP_HOST = "http://localhost:8080/pipeline"  # e.g. localhost:8080 or LoadBalancer
# ============================


def compile_pipeline():
    """Compile Python pipeline into a YAML spec."""
    compiler.Compiler().compile(
        pipeline_func=ml_pipeline,
        package_path=PIPELINE_FILE,
    )
    print(f"✅ Compiled pipeline saved to {PIPELINE_FILE}")


def upload_pipeline(client: Client):
    """Upload pipeline spec to KFP UI (or update if exists)."""
    try:
        pipeline = client.get_pipeline_id(PIPELINE_NAME)
        if pipeline:
            print(f"🔄 Pipeline '{PIPELINE_NAME}' exists, uploading new version...")
            client.upload_pipeline_version(
                pipeline_package_path=PIPELINE_FILE,
                pipeline_version_name="v1",   # you can increment this
                pipeline_id=pipeline,
            )
        else:
            print(f"⬆️ Uploading new pipeline '{PIPELINE_NAME}'...")
            client.upload_pipeline(
                pipeline_package_path=PIPELINE_FILE,
                pipeline_name=PIPELINE_NAME,
            )
    except Exception as e:
        print(f"❌ Failed to upload pipeline: {e}")
        raise


def run_pipeline(client: Client):
    """Run pipeline inside an experiment."""
    experiment = client.create_experiment(EXPERIMENT_NAME)
    run = client.run_pipeline(
        experiment_id=experiment.id,
        job_name=RUN_NAME,
        pipeline_package_path=PIPELINE_FILE,
        params={},   # pass pipeline params if needed
    )
    print(f"🚀 Run started: {RUN_NAME}")
    return run


if __name__ == "__main__":
    # Step 1. Compile
    compile_pipeline()

    # Step 2. Connect to KFP
    client = Client(host=KFP_HOST)

    # Step 3. Upload
    upload_pipeline(client)

    # Step 4. Run
    run_pipeline(client)


