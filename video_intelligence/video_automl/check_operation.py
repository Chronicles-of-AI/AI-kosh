from google.cloud import automl
from google.longrunning.operations_proto_pb2 import Operation

client = automl.AutoMlClient()


def get_operation_details(operation_id: str):
    try:
        response = client._transport.operations_client.get_operation(operation_id)
        if response.done:
            if response.error.code != 0:
                operation_status = "Failed"
                error_message = response.error.message
            else:
                operation_status = "Success"
                error_message = ""
        else:
            operation_status = "In-Progress"
            error_message = ""
        return {
            "operation_id": operation_id,
            "operation_completed": response.done,
            "status_metadata": operation_status,
            "error_message": error_message,
        }
    except Exception as error:
        raise error


operation_id = "LONG_RUNNING_OPERATION_ID"
status = get_operation_details(operation_id=operation_id)
print(f"operation status : {status}")
