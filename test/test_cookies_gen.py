#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/10/12 19:02
@Description: 
"""
from WeChatSpider.cookies import get_cookies


class TestCookiesGen(object):
    def test_cookies_gen(self):
        cookies = get_cookies()
        print(cookies)
