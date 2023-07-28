from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.dags.api_call_to_gcs import call_api_and_upload_to_gcs
import requests
import pandas as pd
from google.cloud import storage

def call_api_and_upload_to_gcs():
    # Your API call to get data
    response = requests.get('https://opensky-network.org/api/states/all')
    data = response.json()['states']
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M")

    schema = {
    'icao24': str,
    'callsign': str,
    'origin_country': str,
    'time_position': 'Int64',
    'last_contact': 'Int64',
    'longitude': float,
    'latitude': float,
    'geo_altitude': float,
    'on_ground': bool,
    'velocity': float,
    'true_track': float,
    'vertical_rate': float,
    'sensors': str,
    'baro_altitude': float,
    'squawk': str,
    'spi': bool,
    'category': 'Int64',
    }

    df = pd.DataFrame(data, columns=schema.keys()).astype(schema)
    csv_content = df.to_csv(index=False)

    # Upload data to Google Cloud Storage
    gcs_client = storage.Client()
    bucket_name = 'opensky-api-extraction'
    blob_name = f'hourly-extraction/{formatted_date}-opensky_data.csv'
    bucket = gcs_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(csv_content)

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
    destination_project_dataset_table='opensky-api-394212.test_api.test_table',
    write_disposition='WRITE_APPEND',
    dag=dag,
)

call_api_task >> gcs_to_bq_task