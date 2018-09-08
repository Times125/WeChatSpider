#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/4 16:18
@Description: Fake Chrome UA
"""
import random


__all__ = ['ChromeUA', 'headers']

first_num = random.randint(55, 69)
third_num = random.randint(0, 3500)
fourth_num = random.randint(0, 140)


class ChromeUA:
    os_type = [
                '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
                '(Macintosh; Intel Mac OS X 10_13_6)'
               ]

    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    @classmethod
    def get_ua(cls):
        return ' '.join(['Mozilla/5.0', random.choice(cls.os_type), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', cls.chrome_version, 'Safari/537.36']
                        )


headers = {
    'User-Agent': ChromeUA.get_ua(),
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive'
}
