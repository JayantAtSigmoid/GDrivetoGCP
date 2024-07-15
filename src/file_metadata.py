import os
import json

METADATA_FILE = 'file_metadata.json'

def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_metadata(metadata):
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f)

def get_file_size(file_content):
    file_content.seek(0, os.SEEK_END)
    size = file_content.tell()
    file_content.seek(0)  # Reset the pointer
    return size
