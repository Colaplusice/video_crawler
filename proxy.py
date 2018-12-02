import requests
from bs4 import BeautifulSoup

from configs import MAIN_PAGE_URL,HEADERS
# 请求地址
# targetUrl = "http://baidu.com"
targetUrl = "http://www.showmemyip.com/"

# 代理服务器
proxyHost = "39.137.69.10"
proxyPort = 80
# host = '111.7.130.101'
from functools import lru_cache


# proxyMeta = "http://%(host)s:%(port)s" % {"host": proxyHost, "port": proxyPort}
#
# proxies = {"http": proxyMeta, "https": proxyMeta}
#
# resp = requests.get(targetUrl, proxies=proxies)
# print(resp.status_code)
# print(resp.text)

@lru_cache(maxsize=2)
def get_proxy_ip():
    ip_source = 'http://cn-proxy.com/'
    # ip_source = 'http://baidu.com/'
    res = requests.get(url=ip_source, headers=HEADERS)
    print(res.status_code)
    assert res.status_code == 200


def extract_proxy_ip(html):
    if not html:
        raise FileNotFoundError('html is null')
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find("div", {"class": "sortable"})
    if not tables:
        raise FileNotFoundError('div is null')

    for tr in tables.find('tr'):
        print(tr)


if __name__ == '__main__':
    html = get_proxy_ip()
    extract_proxy_ip(html)
