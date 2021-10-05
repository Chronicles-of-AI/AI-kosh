import boto3

client = boto3.client("textract", region_name="us-east-2")

response = client.analyze_expense(
    Document={
        "S3Object": {
            "Bucket": "mlops-documents-dataset",
            "Name": "merged_invoice_Page_1_Image_0001.jpg",
        }
    }
)
print(response)
