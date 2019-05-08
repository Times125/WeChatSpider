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
from werkzeug.contrib.cache import FileSystemCache

__all__ = ['suv_gen', 'CookiesCache']


def suv_gen():
    mills = round(time.time() * 1000)
    a = mills * 1e3
    b = round(1e3 * random.random())
    c = str(int(a + b))
    hl = hashlib.md5()
    hl.update(c.encode('utf-8'))
    return hl.hexdigest()


class CookiesCache(FileSystemCache):
    """
    缓存有效的cookies
    """

    def __init__(self, cache_path='./tmp/cookie-cache', default_timeout=300):
        super(CookiesCache, self).__init__(cache_path, default_timeout)

    def get(self, key):
        try:
            return super(CookiesCache, self).get(key)
        except ValueError:
            return None
