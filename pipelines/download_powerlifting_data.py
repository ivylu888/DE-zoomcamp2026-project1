import io
import pandas as pd
import requests
from zipfile import ZipFile

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data_from_api(*args, **kwargs):
    url = 'https://openpowerlifting.gitlab.io/opl-csv/files/openpowerlifting-latest.zip'
    response = requests.get(url)
    with ZipFile(io.BytesIO(response.content)) as myzip:
        csv_filename = [name for name in myzip.namelist() if name.endswith('.csv')][0]
        with myzip.open(csv_filename) as csv_file:
            df = pd.read_csv(csv_file, low_memory=False)
    print(f" Successfully loaded {len(df)} rows from {url}")
    return df