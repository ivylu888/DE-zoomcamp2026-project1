import os
import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_bigquery(*args, **kwargs) -> None:
    project_id = os.environ.get('GCP_PROJECT_ID')
    bucket_name = os.environ.get('GCP_GCS_BUCKET_NAME')
    dataset = 'powerlifting_data'
    table = 'raw_powerlifting'

    gcs_path = f'gs://{bucket_name}/raw_powerlifting_data.parquet'
    print(f"📖 從 GCS 讀取：{gcs_path}...")
    
    df = pd.read_parquet(
        gcs_path,
        storage_options={
            "project": project_id,
            "token": os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        }
    )
    
    print(f"✅ 讀取完成！共 {len(df)} 筆，載入 BigQuery...")

    df.to_gbq(
        destination_table=f'{dataset}.{table}',
        project_id=project_id,
        if_exists='replace'
    )
    print(f"✅ 完工！")