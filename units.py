import requests
import urllib3
import math
import json
import pandas as pd

urllib3.disable_warnings()

csv_file_datasource = 'data/data_konstruksi.csv'
csv_file_datastore = 'data/unit_konstruksi.csv'

# Function
def get_items(idskk, page, storage):

    url = 'https://bnsp.go.id/man.ajax.php'

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://bnsp.go.id',
        #'Referer': 'https://bnsp.go.id/skk',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
    }
    
    data = {
        'ajax': '1',
        'mode': 'mod',
        'cl': 'daftarskk',
        'ikdata[0]': 'getskkunit',
        'ikdata[idskk]': f'{idskk}',
        'ikdata[halaman]': f'{page}',
        #'ikdata[nama]': '',
    }

    response = requests.post(url=url, headers=headers, data=data, verify=False)

    unit_raw = response.text.replace('{"data":', '').split(',"halaman":')
    unit_items = unit_raw[0]
    
    unit_items = json.loads(unit_items)
    storage.extend(unit_items)


# Parameters
prev_data = pd.read_csv(csv_file_datasource)
id_skk_list = prev_data['Id'].to_list()
n_units = prev_data['Unit Counts'].to_list()
n_pages = [math.ceil(int(u)/30) for u in n_units]

# Main process
datastore = []
for n in range(len(id_skk_list)):
    for p in range(1, n_pages[n]+1):
        try:
            get_items(id_skk_list[n], p, datastore)
        except:
            continue

# Save data
name_dict = {
    'id': 'Id Unit', 
    'idskk' : 'Id', 
    'kode': 'Code', 
    'nama': 'Name', 
    'keterangan': 'Desctiption',
    'status': 'Status'
}
df_dataunit = pd.DataFrame(datastore)
df_dataunit.rename(columns = name_dict, inplace = True)
df_dataunit.to_csv(csv_file_datastore, index = False)

print(f'''Unit data saved to "{csv_file_datastore}" with {len(df_dataunit.index)} records''')
