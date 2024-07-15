from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'drive_to_gcs_dag',
    default_args=default_args,
    description='A DAG to download a file from Google Drive and upload to GCS every week',
    schedule_interval=timedelta(weeks=1),
)

run_python_script = BashOperator(
    task_id='run_drive_to_gcs_script',
    bash_command='python3 /Users/jayantasudhani/airflow/src/main.py',
    dag=dag,
)

run_python_script
