from google.cloud import automl_v1beta1 as automl

client = automl.AutoMlClient()


def get_model_evaluation(model_id: str, project_id: str, model_evaluation_id: str):
    # Get the full path of the model evaluation.
    model_path = client.model_path(project_id, "us-central1", model_id)
    model_evaluation_full_id = f"{model_path}/modelEvaluations/{model_evaluation_id}"

    # Get complete detail of the model evaluation.
    response = client.get_model_evaluation(name=model_evaluation_full_id)

    print("Model evaluation name: {}".format(response.name))
    print("Model annotation spec id: {}".format(response.annotation_spec_id))
    print("Create Time: {}".format(response.create_time))
    print("Evaluation example count: {}".format(response.evaluated_example_count))

    print(
        "Classification model evaluation metrics: {}".format(
            response.classification_evaluation_metrics
        )
    )


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


model_id = ""
project_id = ""
model_evaluation_id = ""  # can be retrived from get_model_description function
input_uri = ""
output_uri = ""
batch_predict(
    model_id=model_id, project_id=project_id, input_uri=input_uri, output_uri=output_uri
)
get_model_evaluation(
    model_id=model_id, project_id=project_id, model_evaluation_id=model_evaluation_id
)
