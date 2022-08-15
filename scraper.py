import requests
import urllib3
import pandas as pd
from bs4 import BeautifulSoup

urllib3.disable_warnings()


csv_file_datastore = 'data/data.csv'
keyword = 'konstruksi'

# General setting for requests
url = 'https://bnsp.go.id/skk'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US;q=0.9',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36',
}

# Initial request
response = requests.get(url = url, headers = headers, verify = False)
page = BeautifulSoup(response.text, 'html.parser')

# Get the last page
for option in page.find('select', {'id':'sl_halaman'}).find_all('option')[-1:]:
    lastpage = int(option.text)

# Get metadata
metadata = []
footer = page.find('div', class_ = 'footer_profile_info')
for item in footer.find_all('div'):
    meta = item.text.strip().split('\n')
    if len(meta) == 1 and meta[0] != '':
        metadata.append(meta[0])


names = []
description = []
types = []
adjudication = []
date_adjusment = []
item_count = []


# Full requests
for p in range(1, lastpage+1):
#for p in range(1, 1+1): # for development purpose

    params = {'namaskk': f'{keyword}', 'page': f'{p}'}    
    response = requests.get(url=url, params=params, headers=headers, verify=False)
    page = BeautifulSoup(response.text, 'html.parser')

    # Parsing data
    for name in page.find_all('div', class_ = 'nama_skk'):
        names.append(name.text.strip())

    for desc in page.find_all('div', class_ = 'keterangan_skk'):
        description.append(desc.text.strip())

    for type in page.find_all('div', class_ = 'jenis_skk'):
        types.append(type.find('div', class_ = 'skk_data_kanan').text.strip())

    for adj in page.find_all('div', class_ = 'kepmen_skk'):
        adjudication.append(adj.find('div', class_ = 'skk_data_kanan').text.strip())

    for dateadj in page.find_all('div', class_ = 'tanggal_skk'):
        date_adjusment.append(dateadj.find('div', class_ = 'skk_data_kanan').text.strip())

    for ic in page.find_all('div', class_ = 'jumlahunit_skk'):
        item_count.append(int(ic.find('div', class_ = 'data_jumlah_skk').text.strip()))
    

# Store data
data = {
    'Name': names,
    'Description': description,
    'Type': types,
    'Adjudication': adjudication, # kepmen
    'Adjustment Date': date_adjusment,
    'Unit Counts': item_count
}

metadata = {
    'Description': metadata[3],
    'Address': metadata[0],
    'Phone': metadata[1],
    'Email': metadata[2]
}

df = pd.DataFrame(data)
df.to_csv(csv_file_datastore, index = False)

print(f'Data saved to {csv_file_datastore} with {len(df.index)} rows of record')
print(f'Metadata:\n{metadata}')
