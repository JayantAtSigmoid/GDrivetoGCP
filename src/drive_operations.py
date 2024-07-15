import io
import logging
from file_metadata import get_file_size
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from config import DRIVE_API_CREDS, DRIVE_API_SCOPES


def authenticate_drive():
    """Authenticates and builds a Drive API service."""
    logging.info("Authenticating with Google Drive API.")
    credentials = service_account.Credentials.from_service_account_file(
        DRIVE_API_CREDS, scopes=DRIVE_API_SCOPES)
    drive_service = build('drive', 'v3', credentials=credentials)
    logging.info("Authenticated with Google Drive API.")
    return drive_service

def list_files_in_drive_folder(drive_service, folder_id):
    """Lists all files in a Google Drive folder and their sizes."""
    try:
        logging.info("Listing files in Google Drive folder.")
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents and mimeType='text/csv'",
            pageSize=1000,
            fields="nextPageToken, files(id, name, size)"
        ).execute()
        items = results.get('files', [])
        logging.info(f"Found {len(items)} files in the folder.")
        return items
    except Exception as e:
        logging.error(f"Error listing files in Google Drive folder: {e}")
        return []


def download_file_from_drive(drive_service, file_id, file_name):
    """Downloads file content from Google Drive and returns its content and size."""
    try:
        logging.info(f"Downloading file '{file_name}' with ID: {file_id}.")
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                logging.info(f"Download {int(status.progress() * 100)}% complete for file '{file_name}'.")

        fh.seek(0)  # Rewind the file pointer
        size = get_file_size(fh)
        logging.info(f"Downloaded file '{file_name}' with ID: {file_id} (size: {size} bytes).")
        return fh, size
    except Exception as e:
        logging.error(f"Error downloading file '{file_name}' from Google Drive: {e}")
        return None, None