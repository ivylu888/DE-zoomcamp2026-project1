import io
import pandas as pd
import requests
from zipfile import ZipFile

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(*args, **kwargs):
    url = 'https://openpowerlifting.gitlab.io/opl-csv/files/openpowerlifting-latest.zip'
    print("正在下載壓縮檔，請稍候...")
    response = requests.get(url)
    
    with ZipFile(io.BytesIO(response.content)) as myzip:
        csv_filename = [name for name in myzip.namelist() if name.endswith('.csv')][0]
        with myzip.open(csv_filename) as csv_file:
            df = pd.read_csv(csv_file, low_memory=False)
            
    print(f"成功載入！共 {len(df)} 筆紀錄。")
    return df

@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert len(output) > 0, '下載失敗！'