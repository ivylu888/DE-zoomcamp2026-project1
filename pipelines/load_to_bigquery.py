import os
import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_bigquery(*args, **kwargs) -> None:
    project_id = os.environ.get('GCP_PROJECT_ID')
    bucket_name = os.environ.get('GCP_GCS_BUCKET_NAME')
    gcs_path = f'gs://{bucket_name}/raw_powerlifting_data.parquet'
    df = pd.read_parquet(
        gcs_path,
        storage_options={
            "project": project_id,
            "token": os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        }
    )
    df.to_gbq(
        destination_table='powerlifting_data.raw_powerlifting',
        project_id=project_id,
        if_exists='replace'
    )
    print(f"Done exporting data to BigQuery")