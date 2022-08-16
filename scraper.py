import requests
import urllib3
import time
import pandas as pd
from bs4 import BeautifulSoup

urllib3.disable_warnings()


keyword = 'konstruksi'

csv_file_datastore = f'data/data_{keyword}.csv'

# Metadata settings
csv_file_metadata = 'data/metadata.csv'
date_scraping = time.strftime('%F %H:%M %Z', time.localtime())

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


id_unit = []
names = []
description = []
types = []
adjudication = []
date_adjusment = []
unit_count = []


# Full requests
#for p in range(1, lastpage+1):
for p in range(1, 1+1): # for development purpose

    params = {'namaskk': f'{keyword}', 'page': f'{p}'}    
    response = requests.get(url=url, params=params, headers=headers, verify=False)
    page = BeautifulSoup(response.text, 'html.parser')

    # Parsing data
    for item in page.find_all('div', class_ = 'box_data_skk_main'):
        
        try:
            idu = item.find('div', class_ = 'dokumen_pdf')['onclick']
            idu = idu.replace('daftarskk.bukadokumen({"id":', '').replace(',"tipe":"pdf"})', '')
        except:
            idu = None
        id_unit.append(idu)

        names.append(item.find('div', class_ = 'nama_skk').text.strip())

        description.append(item.find('div', class_ = 'keterangan_skk').text.strip())

        type = item.find('div', class_ = 'jenis_skk')
        types.append(type.find('div', class_ = 'skk_data_kanan').text.strip())

        adj = item.find('div', class_ = 'kepmen_skk')
        adjudication.append(adj.find('div', class_ = 'skk_data_kanan').text.strip())

        dateadj = item.find('div', class_ = 'tanggal_skk')
        date_adjusment.append(dateadj.find('div', class_ = 'skk_data_kanan').text.strip())

        uc = item.find('div', class_ = 'jumlahunit_skk')
        unit_count.append(int(uc.find('div', class_ = 'data_jumlah_skk').text.strip()))
    
# Store data
data = {
    'Id': id_unit,
    'Name': names,
    'Description': description,
    'Type': types,
    'Adjudication': adjudication, # kepmen
    'Adjustment Date': date_adjusment,
    'Unit Counts': unit_count
}

metadata = {
    'Description': [metadata[3]],
    'Address': [metadata[0]],
    'Phone': [metadata[1]],
    'Email': [metadata[2]],
    'Data Date': date_scraping
}

df_data = pd.DataFrame(data)
df_data.to_csv(csv_file_datastore, index = False)

df_metadata = pd.DataFrame(metadata)
df_metadata.to_csv(csv_file_metadata, index = False)

print(f'Data saved to {csv_file_datastore} with {len(df_data.index)} records')
#print(f'Metadata:\n{metadata}')