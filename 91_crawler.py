import requests
from bs4 import BeautifulSoup
import csv

# from tqdm import tqdm
import os
import time

dir_path = os.path.dirname(__file__)


class NoCrawler:
    def __init__(self):
        self.max_page = 0
        self.base_url = 'http://92.91p26.space/v.php?next=watch'
        self.page_url = 'http://92.91p26.space/v.php?next=watch&page={}'
        self.headers = self._load_headers()
        self.video_headers = self._load_headers('headers/video_headers')

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
    def fetch_and_save_html(self):
        html_path = os.path.join(dir_path, 'html')
        if not os.path.exists(html_path):
            os.mkdir(html_path)
        for i in range(1, self.max_page):
            # 判断是否有缓存
            file_path = os.path.join(dir_path, 'html/{}.html'.format(i))
            if os.path.exists(file_path):
                print('从缓存中加载{}html'.format(i))
            else:
                url = self.page_url.format(i)
                html = requests.get(url, headers=self.headers).text
                open(file_path, 'w', encoding='utf-8').write(html)
                print('第{}页抓取完成! url为{}'.format(i, url))
                print('将{}html写入缓存'.format(i))
                time.sleep(3)

    def _load_headers(self, header_file='headers/headers'):
        headers = {}
        with open(header_file) as opener:
            header_line = opener.readlines()
            for header in header_line:
                header = ''.join(header.split(' '))
                item = header.strip().split(':')
                headers[item[0]] = item[1]
        return headers

    def get_and_save_video_html_url(self):

        for i in range(1, self.max_page):
            if not os.path.exists('message/{}.csv'.format(i)):
                with open('html/{}.html'.format(i), 'r') as opener:
                    html_page = opener.read()

                if not html_page:
                    raise FileNotFoundError('html文件不存在!')

                soup = BeautifulSoup(html_page, 'html.parser')
                channels = soup.find_all('div', {'class': 'listchannel'})
                write_opener = open('message/{}.csv'.format(i), 'w', encoding='utf-8')
                csv_writer = csv.writer(write_opener)
                for channel in channels:
                    message_dict = {}
                    href = channel.find('a')['href']
                    message_dict['url'] = href
                    span_info = channel.find_all('span', {'class': 'info'})
                    for each_span in span_info:
                        message_dict[each_span.string] = each_span.next_sibling.strip()
                    keys = message_dict.keys()
                    csv_writer.writerow(keys)

    def get_and_save_video_url(self):
        video_url = 'http://91.91p26.space/view_video.php?viewkey=f3ba33dc25f2434683d1&page=1&viewtype=detailed&category=mr'
        response = requests.get(video_url, headers=self.headers)
        html = response.text
        with open('video/video_html', 'w', encoding='utf-8') as opener:
            opener.write(html)

    def main(self):
        self.get_page_number()
        self.fetch_and_save_html()
        self.get_and_save_video_html_url()

    # def parse_video_url(self):
    #     with open('video/video_html', 'r', encoding='utf-8') as opener:
    #         html = opener.read()
    #     soup = BeautifulSoup(html, 'html.parser')
    #     video_url = soup.find('video').find('source')['src']
    #     print(video_url)
    #     resonse = requests.get(url=video_url, headers=self.video_headers)
    #
    #     print(resonse.status_code)
    #     video_path = 'video/{}'
    #     # if resonse.status_code==200:
    #     for i in resonse.iter_content(chunk_size=1024):
    #         print(i)
    #     with open(video_path.format(1), 'wb') as opener:
    #         for chunck in tqdm(resonse.iter_content(chunk_size=1024)):
    #             opener.write(chunck)
    #     print('写入成功')
    #     print(video_url)

    def download_video(self):
        pass

    def _write_to_database(self):
        pass


#
if __name__ == '__main__':
    crawler = NoCrawler()
    crawler.main()
