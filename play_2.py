import requests

url = 'http://185.38.13.130//mp43/284712.mp4?st=6dwhzemeT58Crf8E_x7WmA&e=1538895505'
headers = _get_headers('video_headers')

res = requests.get(url, headers=headers)
length = res.headers.get('Content-Length'
                         )

# block_size = length // 1024
# for i in range(1, block_size + 1):
headers['range'] = "bytes=%s-%s" % (0, length)

res=requests.get(url,headers=headers,stream=True)

with open('sd.mp4','ab')as f:
    for chuck in res.iter_content(chunk_size=1024):
        f.write(chuck)

print('success')
