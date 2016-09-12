#_*_coding:utf-8_*_
import requests
import threading
from bs4 import BeautifulSoup
from  requests.exceptions import ConnectionError
headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTlhZmZmNjg1ZjY3M2M3MDk3ZDQ5MDQyYzRmOWIwYWMzBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWtGbnh6VXVNZlpkYUovTHg5bnpJd2tzN2hTK0xYMDJKdHIrQ2s2RVptY0k9BjsARg%3D%3D--7fb9e4d16564e4f99e5cc22f0bf93e44e522ab6e; CNZZDATA1256960793=713396777-1466048187-null%7C1466048187',
    'Host':'www.xicidaili.com',
    'Referer':'https://www.baidu.com/link?url=1iVmjIi0KFvtc3G_a4cDTq7PUl_PX3i6b5n_2tSfRVs5CTiVpzym7v120BIVo89a&wd=&eqid=f8676aab001fd4ca0000000357622406',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
}

r = requests.get('http://www.xicidaili.com',headers=headers)
soup = BeautifulSoup(r.text.encode(r.encoding).decode('utf-8'),"lxml")
proxies_list = []
for i in  soup.find_all('tr'):
    try:
        if i.contents[9].string == u'高匿':
            ip = i.contents[3].string
            port = i.contents[5].string
            proxy_ip_type = i.contents[9].string
            proxy_pro_type = i.contents[11].string
            if proxy_pro_type == 'HTTP':
                proxies_list.append({'http':'http://%s:%s' % (ip,port)})
            elif proxy_pro_type == 'HTTPS':
                proxies_list.append({'https':'http://%s:%s'% (ip,port)})
            else:
                proxies_list.append({'https':'socks4://%s:%s'% (ip,port)})
                proxies_list.append({'https':'socks5://%s:%s'% (ip,port)})



    except IndexError:
        pass
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'If-Modified-Since':'Wed, 13 Apr 2016 04:18:54 GMT',
    'If-None-Match':"1609da-17-53056136232bf",
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36 '
}



bad_proxys = []

def url_request(proxies):
    try:
        r = requests.get('http://www.baidu.com',headers=headers,proxies=proxies,timeout=5)
#        print r.text
    except Exception:
        bad_proxys.append(proxies)

threads = []
for proxies in proxies_list:
    t = threading.Thread(target=url_request,args=(proxies,))
    t.start()
    threads.append(t)


for t in threads:
    t.join()


print len(proxies_list)
print len(bad_proxys)
