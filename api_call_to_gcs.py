import requests
import pandas as pd
from datetime import datetime
from google.cloud import storage

def call_api_and_upload_to_gcs():
    # Your API call to get data
    response = requests.get('https://opensky-network.org/api/states/all')
    data = response.json()['states']
    date_now = datetime.now()

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
    bucket_name = 'opensky-api-data'
    blob_name = f'hourly-extraction/{date_now}-opensky_data.csv'
    bucket = gcs_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(csv_content)

call_api_and_upload_to_gcs()