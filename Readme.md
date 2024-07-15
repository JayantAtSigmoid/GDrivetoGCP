# Google Drive to Google Cloud Storage Data Transfer

This project contains scripts to automate the process of downloading CSV files from a Google Drive folder, appending new data to an existing file stored in Google Cloud Storage (GCS), and uploading the updated file back to GCS. The script also maintains metadata to avoid re-downloading unchanged files.


## Files Description

- `airflow-webserver.pid`, `airflow.cfg`, `airflow.db`, `logs/`, `webserver_config.py`: Airflow-related files.
- `dags/weekly_transfer_dag.py`: Airflow DAG definition for scheduling the data transfer script.
- `file_metadata.json`: Stores metadata (file names and sizes) of previously processed files to avoid redundant downloads.
- `requirements.txt`: Lists Python dependencies.
- `src/`: Contains the main Python scripts for data transfer.
  - `__init__.py`: Marks the directory as a Python package.
  - `config.py`: Contains configuration constants such as API credentials and folder IDs.
  - `data_processing.py`: Contains functions to append new data to the existing file.
  - `drive_operations.py`: Contains functions to interact with Google Drive, including authentication, listing files, and downloading files.
  - `gcs_operations.py`: Contains functions to interact with Google Cloud Storage, including downloading and uploading files.
  - `main.py`: The main script that orchestrates the data transfer process.

## Setup Instructions

### Prerequisites

1. Python 3.6 or higher.
2. Required Python packages listed in `requirements.txt`.
3. Google Cloud Platform service account with appropriate permissions.
4. Google Drive API enabled for your project.

### Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/JayantAtSigmoid/GDrivetoGCP.git
    cd data-transfer
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Update the `config.py` file with your Google Drive and Google Cloud credentials.

### Usage

1. Run the main script:
    ```sh
    python src/main.py
    ```

### Scheduling with Airflow

1. Ensure Airflow is installed and running.
2. Add the `weekly_transfer_dag.py` to your Airflow DAGs folder.
3. Start the Airflow scheduler to run the DAG as per the defined schedule.

## Metadata Handling

The script keeps track of the files and their sizes in a local file (`file_metadata.json`). Before downloading any file, it checks the metadata to avoid downloading unchanged files.

## Logs

Logs are printed to the console to provide real-time feedback about the script's execution.

## Limitations

- Ensure your machine has sufficient memory (RAM) to handle the size of files being processed. For a machine with 8GB RAM, you can typically handle files up to 1-2GB comfortably, depending on other running processes.

## Contributing

Contributions are welcome. Please create a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
