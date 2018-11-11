from download_flag.configs import CC_LIST, DEST_DIR, BASE_URL
from utils import timer
import requests
import os


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as f:
        f.write(img)


def get_flag(cc):
    res = requests.get(url=BASE_URL.format(country=cc))
    return res.content


def show(text):
    print(text,end=' ')


def download_many(cc_list):
    for cc in cc_list:
        image = get_flag(cc)
        save_flag(image, '{}.gif'.format(cc))
        show(cc)


@timer
def main(download_many):
    download_many(CC_LIST)


if __name__ == '__main__':
    main(download_many)
