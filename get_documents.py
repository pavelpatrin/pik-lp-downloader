import datetime
import os
import requests

API_URL = 'https://api.pik.ru/v1/developer?get=documents&block_id=233'
API_HEADERS = {
    'Referer': 'http://aotechnostroy.ru/',
    'Origin': 'http://aotechnostroy.ru',
}

response = requests.get(API_URL, headers=API_HEADERS)
print('Got index response (%d bytes)' % len(response.content))

data_root = str(datetime.datetime.now())
print('Saving all data to %s' % data_root)

os.mkdir(data_root)
with open('%s/documents.json' % data_root, 'wb') as fh:
    fh.write(response.content)

urls = [
    doc['url']
    for project in response.json().get('projects', [])
    for bulk in project.get('bulks', [])
    for doc in bulk.get('docs', [])
]

print('Downloading %d urls' % len(urls))
for index, url in enumerate(urls):
    print('Downloading %s' % url)
    response = requests.get(url, headers=API_HEADERS)
    filename = '%d-%s' % (index, url.split('/')[-1])
    with open('%s/%s' % (data_root, filename), 'wb') as fh:
        fh.write(response.content)
