# -*- coding:utf-8 -*- 
import requests
import time
import hashlib
import re


def login():
    
    login_dict = {
        'loginName' : '18702289268',
        'pwd' : '123abc,.',
        'captcha' : '',
    }

    login_res = requests.post(
        url= "https://passport.xebest.com/login/login.shtml",
        data=login_dict,
        headers={
            'Referer': 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN',
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, sdch, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Host':'passport.xebest.com',
            'Referer':'http://www.xebest.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
    )

    # 登陆成功之后获取服务器响应的cookie
    resp_cookies_dict = login_res.cookies.get_dict()
    # 登陆成功后，获取服务器响应的内容
    resp_text = login_res.text
    # 登陆成功后，获取token

    # token = re.findall(".*token=(\d+)", resp_text)[0]
# http://my.xebest.com/myXeHome/getMyHomePage.shtml
    print resp_text
    # print token
    print resp_cookies_dict

login()
