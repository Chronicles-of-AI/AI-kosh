from google.cloud import automl_v1beta1 as automl

project_id = "chronicles-of-ai"
dataset_name = "humanActions"
annotation_csv_uri = "gs://coa_video_ai_automl/annotation_master.csv"

client = automl.AutoMlClient()


def create_dataset(project_id: str, display_name: str):
    """Create a automl video classification dataset."""
    # A resource that represents Google Cloud Platform location.
    project_location = f"projects/{project_id}/locations/us-central1"
    metadata = automl.VideoClassificationDatasetMetadata()
    dataset = automl.Dataset(
        display_name=display_name,
        video_classification_dataset_metadata=metadata,
    )

    # Create a dataset with the dataset metadata in the region.
    created_dataset = client.create_dataset(parent=project_location, dataset=dataset)

    # Display the dataset information
    print("Dataset name: {}".format(created_dataset.name))

    # To get the dataset id, you have to parse it out of the `name` field.
    # As dataset Ids are required for other methods.
    # Name Form:
    #    `projects/{project_id}/locations/{location_id}/datasets/{dataset_id}`
    print("Dataset id: {}".format(created_dataset.name.split("/")[-1]))
    return created_dataset.name.split("/")[-1]


def import_dataset(project_id: str, dataset_id=str, path=str):
    """Import a dataset."""
    # Get the full path of the dataset.
    dataset_full_id = client.dataset_path(project_id, "us-central1", dataset_id)
    # Get the multiple Google Cloud Storage URIs
    input_uris = path.split(",")
    gcs_source = automl.GcsSource(input_uris=input_uris)
    input_config = automl.InputConfig(gcs_source=gcs_source)
    # Import data from the input URI
    response = client.import_data(name=dataset_full_id, input_config=input_config)
    print(f"operation_id : {response.operation.name}")
    return response.operation.name
    # print("Processing import...")
    # print("Data imported. {}".format(response.result()))


def list_datasets(project_id: str):
    """List datasets."""
    # A resource that represents Google Cloud Platform location.
    project_location = f"projects/{project_id}/locations/us-central1"

    # List all the datasets available in the region.
    request = automl.ListDatasetsRequest(parent=project_location, filter="")
    response = client.list_datasets(request=request)

    print("List of datasets:")
    for dataset in response:
        print("Dataset name: {}".format(dataset.name))
        print("Dataset id: {}".format(dataset.name.split("/")[-1]))
        print("Dataset display name: {}".format(dataset.display_name))
        print("Dataset create time: {}".format(dataset.create_time))

        print(
            "Video classification dataset metadata: {}".format(
                dataset.video_classification_dataset_metadata
            )
        )


def delete_dataset(project_id: str, dataset_id: str):
    """Delete a dataset."""
    # Get the full path of the dataset
    dataset_full_id = client.dataset_path(project_id, "us-central1", dataset_id)
    response = client.delete_dataset(name=dataset_full_id)

    print("Dataset deleted. {}".format(response.result()))


# dataset_id = create_dataset(project_id=project_id, display_name=dataset_name)
# dataset_id = "VCN404924293986648064"
# import_dataset_operation_id = import_dataset(
#     project_id=project_id, dataset_id=dataset_id, path=annotation_csv_uri
# )
# list_datasets(project_id=project_id)
# delete_dataset(project_id=project_id, dataset_id=dataset_id)
