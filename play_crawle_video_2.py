import requests
import os
from utils import _get_headers, http_404_exception


def download_video():
    url = 'http://192.240.120.34//mp43/277794.mp4'
    # url = 'http://185.38.13.130//mp43/284712.mp4?st=6dwhzemeT58Crf8E_x7WmA&e=1538895505'
    print('begin')
    headers = _get_headers('headers/video_headers')
    # max_length = headers.get('Range').split('-')[-1]
    path = url.split('/')[-1]

    if os.path.exists(path):
        os.remove(path)

    # print(max_length)
    # partial = 10000
    # each_length = int(max_length) // partial
    # each_length = 8192

    # begin = 1
    opener = open(path, 'wb+')
    try:

        # begin_length = (i - 1) * each_le/ngth
        # end_length = i * each_length
        # headers['Range'] = 'bytes={}-{}'.format(begin_length, end_length)
        # print(headers['Range'])
        res = requests.request(method='GET', url=url, headers=headers, stream=True)
        print(res.status_code)
        if res.status_code == 404:
            raise http_404_exception
        data = res.content
        # if res.status_code == 206:
        opener.write(data)
        #     print('写入成功第{}块'.format(i))
        #     print(res.headers)
        #     data_point = res.headers.get('Content-Range').split('/')[1]
    except http_404_exception:
        print('404')

    print('写入完成')

download_video()
