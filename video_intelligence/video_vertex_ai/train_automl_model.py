from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import trainingjob


def create_training_pipeline_video_classification_sample(
    project: str,
    display_name: str,
    dataset_id: str,
    model_display_name: str,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PipelineServiceClient(client_options=client_options)
    training_task_inputs = (
        trainingjob.definition.AutoMlVideoClassificationInputs().to_value()
    )

    training_pipeline = {
        "display_name": display_name,
        "training_task_definition": "gs://google-cloud-aiplatform/schema/trainingjob/definition/automl_video_classification_1.0.0.yaml",
        # Training task inputs are empty for video classification
        "training_task_inputs": training_task_inputs,
        "input_data_config": {"dataset_id": dataset_id},
        "model_to_upload": {"display_name": model_display_name},
    }
    parent = f"projects/{project}/locations/{location}"
    response = client.create_training_pipeline(
        parent=parent, training_pipeline=training_pipeline
    )
    print("response:", response)


project = "chronicles-of-ai"
display_name = "human_activity_v1"
dataset_id = "994706179416391680"
model_display_name = "human_activity_model_v1"
create_training_pipeline_video_classification_sample(
    project=project,
    display_name=display_name,
    dataset_id=dataset_id,
    model_display_name=model_display_name,
)
