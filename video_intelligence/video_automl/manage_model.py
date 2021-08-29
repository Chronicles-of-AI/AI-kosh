from google.cloud import automl_v1beta1 as automl

# TODO: Update the variable values
project_id = "chronicles-of-ai"
dataset_id = "VCN404924293986648064"
display_name = "HumanActionsModel_v1"

client = automl.AutoMlClient()


def create_model(
    project_id: str,
    dataset_id: str,
    display_name: str,
):
    """Create a automl video classification model."""
    # A resource that represents Google Cloud Platform location.
    project_location = f"projects/{project_id}/locations/us-central1"
    # Leave model unset to use the default base model provided by Google
    metadata = automl.VideoClassificationModelMetadata()
    model = automl.Model(
        display_name=display_name,
        dataset_id=dataset_id,
        video_classification_model_metadata=metadata,
    )

    # Create a model with the model metadata in the region.
    response = client.create_model(parent=project_location, model=model)

    print("Training operation name: {}".format(response.operation.name))
    print("Training started...")
    return response.operation.name


def get_model_details(model_id: str):
    # Get the full path of the model.
    model_full_id = client.model_path(project_id, "us-central1", model_id)
    model = client.get_model(name=model_full_id)
    print(model)
    # Retrieve deployment state.
    if model.deployment_state == automl.Model.DeploymentState.DEPLOYED:
        deployment_state = "deployed"
    else:
        deployment_state = "undeployed"

    # Display the model information.
    print("Model name: {}".format(model.name))
    print("Model id: {}".format(model.name.split("/")[-1]))
    print("Model display name: {}".format(model.display_name))
    print("Model create time: {}".format(model.create_time))
    print("Model deployment state: {}".format(deployment_state))


def get_all_models(project_id: str):
    project_location = f"projects/{project_id}/locations/us-central1"
    request = automl.ListModelsRequest(parent=project_location, filter="")
    response = client.list_models(request=request)

    print("List of models:")
    for model in response:
        # Display the model information.
        if model.deployment_state == automl.Model.DeploymentState.DEPLOYED:
            deployment_state = "deployed"
        else:
            deployment_state = "undeployed"

        print("Model name: {}".format(model.name))
        print("Model id: {}".format(model.name.split("/")[-1]))
        print("Model display name: {}".format(model.display_name))
        print("Model create time: {}".format(model.create_time))
        print("Model deployment state: {}".format(deployment_state))


def delete_model(project_id: str, model_id: str):
    model_full_id = client.model_path(project_id, "us-central1", model_id)

    response = client.delete_model(name=model_full_id)
    print("Model Deletion operation name: {}".format(response.operation.name))
    return response.operation.name


# TODO: Uncomment the function to start training AutoML model
# operation_id = create_model(
#     project_id=project_id,
#     dataset_id=dataset_id,
#     display_name=display_name,
# )
# model_id = "VCN7804691974744702976"
# TODO: Uncomment the function to get details of a trained model
# get_model_details(model_id=model_id)
# TODO: Uncomment the function to get all the trained model under a project
# get_all_models(project_id=project_id)
# TODO: Uncomment the function to delete the trained model
# operation_id = delete_model(project_id=project_id, model_id=model_id)
