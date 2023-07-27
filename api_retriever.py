from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from api_call_to_gcs import call_api_and_upload_to_gcs

now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d %H:%M")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_pipeline',
    default_args=default_args,
    description='A simple data pipeline',
    schedule_interval='@hourly',
    catchup=False,
)

call_api_task = PythonOperator(
    task_id='call_api_and_upload_to_gcs',
    python_callable=call_api_and_upload_to_gcs,
    dag=dag,
)

gcs_to_bq_task = GoogleCloudStorageToBigQueryOperator(
    task_id='gcs_to_bq',
    bucket='opensky-api-data',
    source_objects=[f'hourly-extraction/{formatted_date}-opensky_data.csv'],
    destination_project_dataset_table='opensky-api.test_api.test_table',
    write_disposition='WRITE_APPEND',
    dag=dag,
)

call_api_task >> gcs_to_bq_task