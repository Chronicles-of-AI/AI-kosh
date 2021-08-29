from google.cloud import automl_v1beta1 as automl

client = automl.AutoMlClient()


def get_model_evaluation(
    model_id: str, project_id: str, confidence_threshold: float = 0.85
):
    # Get the full path of the model evaluation.
    model_path = client.model_path(project_id, "us-central1", model_id)
    model_full_id = client.model_path(project_id, "us-central1", model_id)
    for evaluation in client.list_model_evaluations(parent=model_full_id):
        response = client.get_model_evaluation(name=evaluation.name)
        if response.display_name == "":
            for (
                metric
            ) in response.classification_evaluation_metrics.confidence_metrics_entry:
                if metric.confidence_threshold >= confidence_threshold:
                    print(metric)
            print(response.classification_evaluation_metrics.confusion_matrix)


def batch_predict(project_id: str, model_id: str, input_uri: str, output_uri: str):
    """Batch predict"""
    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = automl.AutoMlClient.model_path(project_id, "us-central1", model_id)

    gcs_source = automl.GcsSource(input_uris=[input_uri])

    input_config = automl.BatchPredictInputConfig(gcs_source=gcs_source)
    gcs_destination = automl.GcsDestination(output_uri_prefix=output_uri)
    output_config = automl.BatchPredictOutputConfig(gcs_destination=gcs_destination)
    params = {}

    request = automl.BatchPredictRequest(
        name=model_full_id,
        input_config=input_config,
        output_config=output_config,
        params=params,
    )
    response = prediction_client.batch_predict(request=request)

    print("Waiting for operation to complete...")
    print(
        "Batch Prediction results saved to Cloud Storage bucket. {}".format(
            response.result()
        )
    )


# TODO: Update the variable values
# Trained model id
model_id = "VCN7804691974744702976"
# Project Id
project_id = "chronicles-of-ai"
# CSV path for the video data information
input_uri = "gs://coa_video_ai_automl/batch_prediction.csv"
# Path to save the output of predictions
output_uri = "gs://coa_video_ai_automl/output"
# Predict output label for the video

# TODO: Uncomment the function to get predictions
# batch_predict(
#     model_id=model_id, project_id=project_id, input_uri=input_uri, output_uri=output_uri
# )
# TODO: Uncomment the function to get trained model evaluation
# Get trained model evaluation
# get_model_evaluation(
#     model_id=model_id,
#     project_id=project_id,
#     confidence_threshold=0.9,
# )
