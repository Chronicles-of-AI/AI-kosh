import argparse
import sys

import tritonclient.http as httpclient
from tritonclient.utils import InferenceServerException

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        required=False,
        default=False,
        help="Enable verbose output",
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=False,
        default="localhost:8000",
        help="Inference server URL. Default is localhost:8000.",
    )

    FLAGS = parser.parse_args()
    try:
        triton_client = httpclient.InferenceServerClient(
            url=FLAGS.url, verbose=FLAGS.verbose
        )
    except Exception as e:
        print("context creation failed: " + str(e))
        sys.exit()

    model_name = "intel_image_class"

    # Health
    if not triton_client.is_server_live(query_params={"test_1": 1, "test_2": 2}):
        print("FAILED : is_server_live")
        sys.exit(1)

    if not triton_client.is_server_ready():
        print("FAILED : is_server_ready")
        sys.exit(1)

    if not triton_client.is_model_ready(model_name):
        print("FAILED : is_model_ready")
        sys.exit(1)

    # Metadata
    metadata = triton_client.get_server_metadata()
    if not (metadata["name"] == "triton"):
        print("FAILED : get_server_metadata")
        sys.exit(1)
    print(metadata)

    metadata = triton_client.get_model_metadata(
        model_name, query_params={"test_1": 1, "test_2": 2}
    )
    if not (metadata["name"] == model_name):
        print("FAILED : get_model_metadata")
        sys.exit(1)
    print(metadata)

    # Passing incorrect model name
    try:
        metadata = triton_client.get_model_metadata("wrong_model_name")
    except InferenceServerException as ex:
        if "Request for unknown model" not in ex.message():
            print("FAILED : get_model_metadata wrong_model_name")
            sys.exit(1)
    else:
        print("FAILED : get_model_metadata wrong_model_name")
        sys.exit(1)
