import os
from azure.storage.blob import BlobServiceClient

# Use the standard local Azurite connection string
CONNECTION_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
CONTAINER_NAME = "dietdata"
BLOB_NAME = "All_Diets.csv"
FILE_PATH = "All_Diets.csv"

try:
    print("Connecting to local Azurite Blob Storage...")
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    
    # Create the container if it doesn't exist
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    if not container_client.exists():
        container_client.create_container()
        print(f"Container '{CONTAINER_NAME}' created successfully.")
    
    # Upload the file
    print(f"Uploading {FILE_PATH} to local cloud container...")
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)
    
    with open(FILE_PATH, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
        
    print(f"[SUCCESS] {BLOB_NAME} successfully uploaded to local Azure Emulation storage!")

except Exception as e:
    print(f"[ERROR] Connection failed: {e}")

