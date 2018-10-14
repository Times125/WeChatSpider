#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/27 10:50
@Description: 
"""
import time
import copy
import re
import requests
from bs4 import BeautifulSoup
from WeChatSpider.config import headers
from WeChatSpider.cookies import get_cookies
from WeChatSpider.utils import identify_captcha_by_human
from WeChatSpider.parser import get_total_page, get_data, get_article_content
from WeChatSpider.tasks import crawl_page


# from WeChatSpider.downloader import _unlock


def show_cookies():
    s = requests.session()
    mycookies = dict()
    ajax_action = "http://pb.sogou.com/pv.gif?uigs_productid={}&type=antispider&subtype={}" \
                  "&domain=weixin&suv={}&snuid={}&t={}"
    url = "http://weixin.sogou.com/weixin?type=2&s_from=input&query=%E9%87%8D%E5%A4%A7&ie=utf8&_sug_=n&_sug_type_="
    res = s.get(url, headers=headers)
    print(res.cookies['SNUID'])
    print(res.cookies['SUID'])
    print(res.cookies)
    print(type(res.cookies))
    print(res.text)


def a():
    with open('test.html', 'r', encoding='utf-8') as r:
        html = r.read()
    # num = get_total_page(html)
    # print(num)
    # print(get_data(html))
    con = get_article_content(html)
    print(con)


if __name__ == '__main__':
    # a()
    crawl_page('北京')
    # print(get_cookies())
    # for i in range(50):
    #     url = "https://mp.weixin.qq.com/s?src=11&timestamp=1539423281&ver=1180&signature=jDskjTMxuyHqyHk6Bf52nvpNm8kQAgFxKqtQqVaYGLp0zrnoRbM-ZfFfoV-4MyoFHG3bQCsE-OfW33ibDGWy52-euG7fcoZamsD72Jb4lNAPU8VQE2AAaMQiyr2X2R1W&new=1"
    #     res = requests.get(url, headers=headers)
    #     print(res.url)
    # show_cookies()
    # for i in range(20):
    # refer = "https://weixin.sogou.com/weixin?query=%E6%88%90%E9%83%BD&_sug_type_=&s_from=input&_sug_=n&type=2&page=3&ie=utf8"
    # url = "https://weixin.sogou.com/weixin?query=%E6%88%90%E9%83%BD&_sug_type_=&s_from=input&_sug_=n&type=2&page=3&ie=utf8"
    # re = {"Refer": refer}
    # headers.update(re)
    # res = requests.get(url, headers=headers, cookies=get_cookies(), verify=False)
    # print(res.cookies)
    # print(res.status_code)
    # print(res.url)
    # print(res.text.encode('utf-8').decode('utf8'))
