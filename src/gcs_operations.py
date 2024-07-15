import io
import logging
from google.cloud import storage
from config import GCS_API_CREDS

def download_file_from_gcs(bucket_name, object_name):
    """Downloads file content from Google Cloud Storage."""
    try:
        logging.info(f"Downloading file {object_name} from GCS bucket {bucket_name}.")
        storage_client = storage.Client.from_service_account_json(GCS_API_CREDS)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        if not blob.exists():
            logging.warning(f"File {object_name} does not exist in {bucket_name}.")
            return None
        file_content = io.BytesIO()
        blob.download_to_file(file_content)
        file_content.seek(0)
        logging.info(f"Downloaded file {object_name} from GCS bucket {bucket_name}.")
        return file_content
    except Exception as e:
        logging.error(f"Error downloading file from Google Cloud Storage: {e}")
        return None

def upload_file_to_gcs(bucket_name, object_name, file_content):
    """Uploads file content to Google Cloud Storage."""
    try:
        logging.info(f"Uploading file {object_name} to GCS bucket {bucket_name}.")
        storage_client = storage.Client.from_service_account_json(GCS_API_CREDS)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        blob.upload_from_file(file_content, rewind=True)

        logging.info(f'File {object_name} uploaded to {bucket_name}.')
    except Exception as e:
        logging.error(f"Error uploading file to Google Cloud Storage: {e}")
