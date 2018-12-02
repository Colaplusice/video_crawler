import requests
from utils import _get_headers, http_404_exception

# url = 'http://185.38.13.130//mp43/284712.mp4?st=6dwhzemeT58Crf8E_x7WmA&e=1538895505'
# url = 'http://192.240.120.34//mp43/277794.mp4'
url = 'http://185.38.13.130//mp43/289701.mp4?st=U2q0ZG7xS7Oq0DwDGhSUkA&e=1541983922'

headers = _get_headers('headers/video_headers')

res = requests.get(url, headers=headers)
length = res.headers.get('Content-Length')

# block_size = length // 1024
# for i in range(1, block_size + 1):
headers['range'] = "bytes=%s-%s" % (0, length)

res = requests.get(url, stream=True)
if res.status_code == 404:
    raise http_404_exception

with open('sd.mp4', 'ab') as f:
    for chuck in res.iter_content(chunk_size=1024):
        f.write(chuck)

print('success')
