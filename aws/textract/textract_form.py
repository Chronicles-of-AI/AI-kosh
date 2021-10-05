import boto3

client = boto3.client("textract", region_name="us-east-2")


def read_image_file(path: str):
    with open(path, "rb") as image_file:
        content = image_file.read()
    return {"Bytes": content}


image_path = "/Users/vsatpathy/Desktop/test.png"

image_content = read_image_file(path=image_path)

response = client.analyze_document(
    Document=image_content,
    FeatureTypes=["FORMS"],
)

# In case you want both Tables and Forms in response
# response = client.analyze_document(
#     Document=image_content,
#     FeatureTypes=["FORMS", "TABLES"],
# )

print(response)
