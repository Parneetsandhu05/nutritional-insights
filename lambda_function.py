import os
import pandas as pd
from azure.storage.blob import BlobServiceClient

# Local Azurite configuration string matching our emulator
CONNECTION_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
CONTAINER_NAME = "dietdata"
BLOB_NAME = "All_Diets.csv"
DOWNLOAD_PATH = "extracted_cloud_data.csv"

def lambda_handler(event=None, context=None):
    """
    Simulates a Serverless Cloud Function handler that dynamically
    extracts the nutrition dataset straight from Cloud Storage.
    """
    print("\n--- SERVERLESS CLOUD FUNCTION INITIATED ---")
    try:
        print(f"Connecting to Azure Cloud Storage container: '{CONTAINER_NAME}'...")
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)
        
        print(f"Downloading stream asset '{BLOB_NAME}' from emulation cluster...")
        with open(DOWNLOAD_PATH, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
            
        print(f"Extraction successful! Loading downloaded dataset into Pandas...")
        df = pd.read_csv(DOWNLOAD_PATH)
        
        # Simple extraction verification readout
        total_rows = len(df)
        unique_diets = df['Diet_type'].nunique() if 'Diet_type' in df.columns else "Unknown"
        
        print("\n=== CLOUD DATA METRICS SUMMARY ===")
        print(f"• Total Data Rows Extracted: {total_rows}")
        print(f"• Unique Diet Categories Identified: {unique_diets}")
        print("==================================")
        
        return {
            'statusCode': 200,
            'body': f"Successfully parsed {total_rows} cloud records cleanly."
        }
        
    except Exception as e:
        print(f"[CRITICAL ERROR] Serverless pipeline extraction failed: {e}")
        return {
            'statusCode': 500,
            'body': str(e)
        }

# Allow script to be tested directly via terminal execution
if __name__ == "__main__":
    lambda_handler()
