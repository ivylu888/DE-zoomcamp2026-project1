from pandas import DataFrame
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    bucket_name = os.environ.get('GCP_GCS_BUCKET_NAME')
    project_id = os.environ.get('GCP_PROJECT_ID')
    gcs_path = f'gs://{bucket_name}/raw_powerlifting_data.parquet'
    df.to_parquet(
        gcs_path,
        storage_options={
            "project": project_id,
            "token": os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        }
    )
    print(f"Done exporting data")