import requests
from bs4 import BeautifulSoup
import csv
from disk_cache import DiskCache
from mongo_cache import MongoCache
# from tqdm import tqdm
import sys
import os
import time

from concurrent import futures
import configs
from utils import url2path, timer, _get_headers, http_404_exception
import json

dir_path = os.path.dirname(__file__)


class NoCrawler:
    def __init__(self, cache=MongoCache()):
        self.max_page = 0
        self.base_url = configs.MAIN_PAGE_URL
        self.page_url = configs.EACH_PAGE_URL
        self.headers = self._load_headers()
        self.video_headers = self._load_headers('headers/video_headers')
        self.cache = cache

    # 得到页数
    def get_page_number(self):
        res = requests.get(url=self.base_url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        page_numbers = soup.find('div', {'class': 'pagingnav'})
        max_number = page_numbers.find_all('a')[4].text
        print('总页数为{}'.format(max_number))
        self.max_page = int(max_number)

    def _write_to_csv(self, dict_generator, i):
        with open('message/message{}.csv'.format(i), 'w+', encoding='utf-8') as opener:
            csv_writer = csv.writer(opener)
            for each in dict_generator:
                csv_writer.writerow(each.values())

    # 抓取单页的视频html
    def get_htmls(self, workers=20):
        if isinstance(self.cache, DiskCache):
            html_path = os.path.join(dir_path, 'html')
            if not os.path.exists(html_path):
                os.mkdir(html_path)
        if isinstance(self.cache, MongoCache):
            self.cache.collection_name = 'html'
        page_num = self.max_page
        download_list = []
        for i in range(page_num):
            url = self.page_url.format(i)
            cache_url = url2path(url)
            # 判断是否有缓存
            html_path = '{}.html'.format(cache_url)
            try:
                if self.cache[cache_url]:
                    print('从缓存中加载: {}'.format(html_path))
            except KeyError:
                download_list.append(url)
        with futures.ThreadPoolExecutor(workers) as executor:
            res = executor.map(self.get_html, sorted(download_list))
        return len(list(res))

    def get_html(self, url):
        html = requests.get(url, headers=self.headers).text
        self.text(url)
        self.cache[url2path(url)] = html

    def text(self, i):
        print('将{} 写入缓存'.format(i))

    def _load_headers(self, header_file='headers/headers'):
        headers = {}
        with open(header_file) as opener:
            header_line = opener.readlines()
            for header in header_line:
                header = ''.join(header.split(' '))
                item = header.strip().split(':')
                headers[item[0]] = item[1]
        return headers

    def get_video_urls(self, max_size=None, update=False):
        all = self.cache.items(collection='default')
        max_size = self.cache.length(collection='default')
        self.cache.change_collection(collection_name='video_url')
        if max_size:
            all = list(all)[:max_size]
        with futures.ThreadPoolExecutor(20)as executor:
            res = executor.map(self.get_video_url, all, [update] * max_size)
        print(len(list(res)))

    def get_video_url(self, dic, updated=False):
        key = dic['_id']
        try:
            if self.cache[key] and not updated:
                print('has exist')
                return
        except KeyError:
            pass
        html = dic['key']
        # return
        soup = BeautifulSoup(html, 'html.parser')
        channels = soup.find_all('div', {'class': 'listchannel'})
        message_list = []
        for channel in channels:
            message_dict = {}
            href = channel.find('a')['href']
            title = channel.find('a', title=True)['title']
            message_dict['url'] = href
            message_dict['title'] = title
            span_info = channel.find_all('span', {'class': 'info'})
            for each_span in span_info:
                message_dict[each_span.string] = each_span.next_sibling.strip()
            message_list.append(message_dict)
        self.cache[key] = json.dumps(message_list)
        self.text(key)
        return message_list

    def get_mp4s(self, update=False):
        self.cache.change_collection(collection_name='video_url')
        values = self.cache.values()
        # self.cache.change_collection(collection_name='mp4_url')
        for value in list(values)[:1]:
            print(value)
            for data in value:
                self.get_mp4(data['url'], update)

    def get_mp4(self, url, update=False):
        collection_name = 'mp4_url'
        try:
            if self.cache.get(collection_name=collection_name, key=url) and not update:
                print('get from cache {}'.format(url))
                return
        except KeyError:
            pass
        res = requests.get(url, headers=_get_headers('headers/video_headers'))
        code = res.status_code
        if str(code).startswith('4'):
            print(code)
            sys.exit(1)
        html = res.text
        if not html:
            print(url)
            raise TypeError

        bs4 = BeautifulSoup(html, 'html.parser')
        try:
            mp4_url = bs4.find('source')['src']
            mp4_title = bs4.find('title').split('-')[0]
            data = {'url': mp4_url, 'title': mp4_title}
        except TypeError as e:
            print(html)
            raise
        self.cache.set(collection_name=collection_name, key=url, value=json.dumps(data))
        self.text(url)
        print(mp4_url)
        time.sleep(1)

    def save_videos(self):
        all_mp4_url = self.cache.values(collection='mp4_url')
        print(self.cache.length(collection='mp4_url'))

        with futures.ThreadPoolExecutor(3) as executor:
            executor.map(self.save_video_temp, all_mp4_url)

    def save_video(self, data):
        url = data['url']
        title = data['title']
        collection_name = 'video_name'
        try:
            if self.cache.get(collection_name=collection_name, key=url):
                self.text(url)
                return
        except KeyError:
            print('not in cache')
        res = requests.get(url, stream=True)
        if res.status_code == 404:
            raise http_404_exception
        with open('{}.mp4'.format(title), 'ab')as f:
            for chuck in res.iter_content(chunk_size=1024):
                f.write(chuck)
        print('写入成功: {}'.format(url))
        self.cache.set(collection_name=collection_name, key=url, value=title)
        return title

    def save_video_temp(self, url):
        try:
            if self.cache.get(collection_name='video_name', key=url):
                self.text(url)
                return
        except KeyError:
            print('not in cache')
        res = requests.get(url, stream=True)
        if res.status_code == 404:
            print('not found')
            raise http_404_exception
        with open('{}.mp4'.format(url2path(url)), 'ab')as f:
            for chuck in res.iter_content(chunk_size=1024):
                f.write(chuck)
        print('写入成功: {}'.format(url))
        return url

    def main(self):
        # 得到页数
        # self.get_page_number()
        # 将每页都保存下来
        # self.get_htmls()
        # 得到每页视频的url和信息
        # self.get_video_urls(update=True)
        # 得到 mp4的真实url
        # self.get_mp4s()
        # 保存Mp4
        self.save_videos()

    def login(self):

        pass

    def download_video(self):
        pass

    def _write_to_database(self):
        pass


@timer
def main():
    crawler = NoCrawler(cache=MongoCache(disk_cache=DiskCache(), db_name='video'))
    crawler.main()


#
if __name__ == '__main__':
    main()
