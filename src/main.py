import logging
import sys
import os
import io
import pandas as pd

# Add the src directory to the system path to enable absolute imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from drive_operations import authenticate_drive, list_files_in_drive_folder, download_file_from_drive
from gcs_operations import download_file_from_gcs, upload_file_to_gcs
from data_processing import append_new_data
from file_metadata import load_metadata, save_metadata
from config import DRIVE_FOLDER_ID, GCS_BUCKET_NAME, GCS_OBJECT_NAME

# Configure logging to print to the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def main():
    try:
        drive_service = authenticate_drive()

        # Load previous metadata
        previous_metadata = load_metadata()

        # List all CSV files in the specified Google Drive folder
        files = list_files_in_drive_folder(drive_service, DRIVE_FOLDER_ID)
        current_metadata = {}

        if not files:
            logging.warning("No files found in the specified folder.")
            return

        new_file_contents = []
        metadata_changed = False
        for file in files:
            file_id = file['id']
            file_name = file['name']
            file_size = file.get('size', 0)  # Get the size from the file metadata
            
            current_metadata[file_name] = int(file_size)
            if file_name not in previous_metadata or previous_metadata[file_name] != int(file_size):
                metadata_changed = True
                content, size = download_file_from_drive(drive_service, file_id, file_name)
                if content and size:
                    new_file_contents.append(content)
                else:
                    logging.error(f"Failed to download file '{file_name}' with ID: {file_id}.")
            else:
                logging.info(f"File '{file_name}' has not changed. Skipping.")
        
        if not metadata_changed:
            logging.info("No changes in file metadata. Exiting.")
            return

        # Download existing file content from GCS
        existing_file_content = download_file_from_gcs(GCS_BUCKET_NAME, GCS_OBJECT_NAME)

        if existing_file_content is None:
            # If the file does not exist in GCS, create a new file from the Drive files
            logging.info(f"File {GCS_OBJECT_NAME} does not exist in {GCS_BUCKET_NAME}. Creating a new file from Drive files.")
            combined_df = pd.concat([pd.read_csv(f) for f in new_file_contents]).drop_duplicates(keep='last')
            combined_content = io.BytesIO()
            combined_df.to_csv(combined_content, index=False)
            combined_content.seek(0)
            upload_file_to_gcs(GCS_BUCKET_NAME, GCS_OBJECT_NAME, combined_content)
        else:
            # If the file exists, append the new data
            updated_content = append_new_data(existing_file_content, new_file_contents)
            upload_file_to_gcs(GCS_BUCKET_NAME, GCS_OBJECT_NAME, updated_content)

        # Save current metadata for future reference
        save_metadata(current_metadata)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
