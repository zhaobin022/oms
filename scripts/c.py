#!/usr/bin/env python
# coding=utf-8
# 作者：戴儒锋
# 博客：http://www.linuxyw.com
"""
    脚本功能：
        获取代理IP（国内高匿代理）,使用代理IP是爬虫脚本功能中的一部分

    环境要求：
        1：python版本 2.7.x；
        2：安装bs4库: pip install beautifulsoup4
        3：安装requests库：pip install requests
"""

import re
from random import choice
import requests
import bs4

url = "http://www.xicidaili.com/nn"
headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Referer":"http://www.xicidaili.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
            }

bad_proxys = []
available_proxy = []



def url_request(proxy):
    proxy = 'http://%s' % proxy
    try:
        r = requests.get('http://www.baidu.com',headers=headers,proxies=proxy,timeout=5)
#        print r.text
    except Exception:
        bad_proxys.append(proxy)



all_ips = []
for i in range(1,10):
    r = requests.get(url+str(i),headers=headers)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    data = soup.table.find_all("td")

    ip_compile= re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')
    port_compile = re.compile(r'<td>(\d+)</td>')
    ip = re.findall(ip_compile,str(data))
    port = re.findall(port_compile,str(data))

    ips = [":".join(i) for i in zip(ip,port)]
    all_ips.extend(ips)


for proxy in all_ips:
    url_request(proxy)


print len(all_ips)
print len(bad_proxys)
available_proxy = list(set(all_ips)-set(bad_proxys))
print len(available_proxy)
