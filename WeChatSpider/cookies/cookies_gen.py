#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/10/12 15:02
@Description: 
"""
import hashlib
import random
import time
from WeChatSpider.db import cookies_con
from WeChatSpider.config import cookies_pool

__all__ = ['get_cookies', 'suv_gen']


# 主要是SNUID这个值非常重要
def get_cookies():
    cookie = cookies_con.lpop(cookies_pool)
    cookies = dict()
    if not cookie:
        cookie = (suv_gen(), '80C7D6D3A6A0DEB3264E7B44A6E66BB6')
        # return None
    cookies['SUV'] = cookie[0]
    cookies['SNUID'] = cookie[1]
    return cookies


def suv_gen():
    mills = round(time.time() * 1000)
    a = mills * 1e3
    b = round(1e3 * random.random())
    c = str(int(a + b))
    hl = hashlib.md5()
    hl.update(c.encode('utf-8'))
    return hl.hexdigest()
