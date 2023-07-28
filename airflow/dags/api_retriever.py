from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
import requests
import pandas as pd
from google.cloud import storage, bigquery

def call_api_and_upload_to_gcs():
    # Your API call to get data
    response = requests.get('https://opensky-network.org/api/states/all')
    data = response.json()['states']
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:00")

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
    #blob_name = f'hourly-extraction/{formatted_date}-opensky_data.csv'
    blob_name = 'hourly-extraction/test.csv'
    bucket = gcs_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(csv_content)

def load_csv_to_bigquery():
    bucket_name="opensky-api-extraction"
    dataset_id="test_api"
    table_id="test_table"
    # Initialize the Google Cloud Storage and BigQuery clients
    storage_client = storage.Client()
    bigquery_client = bigquery.Client()

    # Get the GCS bucket and blob
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob("hourly-extraction/test.csv")

    # Define the BigQuery dataset and table
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # Configure the job to load data from GCS to BigQuery
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1  # If CSV has a header row, set this to 1
    job_config.autodetect = True  # Automatically detect schema from CSV

    # Load data into BigQuery
    bigquery_client.load_table_from_uri(
        source_uris=blob,
        destination=table_ref,
        job_config=job_config
    )

now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d %H:00")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2000, 1, 1),
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

"""
gcs_to_bq_task = GoogleCloudStorageToBigQueryOperator(
    task_id='gcs_to_bq',
    bucket='opensky-api-data',
    source_objects=[f'hourly-extraction/{formatted_date}-opensky_data.csv'],
    destination_project_dataset_table='opensky-api-394212.test_api.test_table',
    write_disposition='WRITE_APPEND',
    dag=dag,
    gcp_conn_id='my_custom_gcp_connection'
)
"""

gcs_to_bq_task = PythonOperator(
    task_id='gcs_to_bq_task',
    python_callable=load_csv_to_bigquery,
    dag=dag,
)

call_api_task >> gcs_to_bq_task