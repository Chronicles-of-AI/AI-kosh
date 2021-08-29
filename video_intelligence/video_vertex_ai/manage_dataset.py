from google.cloud import aiplatform


def create_and_import_dataset_video_sample(
    project: str,
    location: str,
    display_name: str,
    src_uris,
    sync: bool = True,
):
    aiplatform.init(project=project, location=location)

    ds = aiplatform.VideoDataset.create(
        display_name=display_name,
        gcs_source=src_uris,
        import_schema_uri=aiplatform.schema.dataset.ioformat.video.classification,
        sync=sync,
    )

    ds.wait()

    print(ds.display_name)
    print(ds.resource_name)
    return ds


project_id = "chronicles-of-ai"
location = "us-central1"
dataset_name = "Activities_v1"
gcs_uri = "gs://coa_video_ai_automl/annotation.csv"
create_and_import_dataset_video_sample(project_id, location, dataset_name, gcs_uri)
