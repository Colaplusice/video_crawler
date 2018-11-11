import requests

# 请求地址
targetUrl = "http://baidu.com"

# 代理服务器
proxyHost = "ip"
proxyPort = "port"

proxyMeta = "http://%(host)s:%(port)s" % {

    "host": proxyHost,
    "port": proxyPort,
}

proxies = {

    "http": proxyMeta,
    "https": proxyMeta,
}

resp = requests.get(targetUrl, proxies=proxies)
print(
    resp.status_code
)
print(resp.text)
