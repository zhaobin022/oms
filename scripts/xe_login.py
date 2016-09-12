# -*- coding:utf-8 -*- 
import requests
import time
import hashlib
import json
import re


requests
LOGIN_COOKIES_DICT = {}

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
    # resp_text = login_res.text
    # 登陆成功后，获取token

    return { 'cookies': resp_cookies_dict}




def get_user_list():

    login_dict = login()
    LOGIN_COOKIES_DICT.update(login_dict)

    login_cookie_dict = login_dict['cookies']
    res_user_list = requests.get(
        url= "http://my.xebest.com/myXeHome/getMyHomePage.shtml",
        cookies = login_cookie_dict,
        headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'my.xebest.com',
            'Referer':'http://www.xebest.com/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        }
    )
    with open('content.txt','w') as f:
        f.write(res_user_list.text)
get_user_list()
