import datetime
import os
import requests

API_URL = 'https://api.pik.ru/v1/news?is_progress=1&is_content=1&only_photo=1&block_id=233'
API_HEADERS = {
    'Referer': 'http://aotechnostroy.ru/',
    'Origin': 'http://aotechnostroy.ru',
}

response = requests.get(API_URL, headers=API_HEADERS)
print('Got index response (%d bytes)' % len(response.content))

data_root = str(datetime.datetime.now())
print('Saving all data to %s' % data_root)

os.mkdir(data_root)
with open('%s/images.json' % data_root, 'wb') as fh:
    fh.write(response.content)

urls = [
    'http://' + image['url'].lstrip('//')
    for date in response.json()
    for image in date.get('images', [])
]

print('Downloading %d urls' % len(urls))
for index, url in enumerate(urls):
    print('Downloading %s' % url)
    response = requests.get(url, headers=API_HEADERS)
    filename = '%d-%s' % (index, url.split('/')[-1])
    with open('%s/%s' % (data_root, filename), 'wb') as fh:
        fh.write(response.content)
