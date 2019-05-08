#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/27 10:50
@Description: 
"""
import time
from WeChatSpider.db import KeywordsOperate, UserMonitorAccount

Base_Url = "http://weixin.sogou.com/weixin?type={}&s_from=input&query={}&ie=utf8&page={}"
account = ['太和智库', '南方智库']

if __name__ == '__main__':
    for it in account:
        data = UserMonitorAccount()
        data.url = Base_Url.format(1, it, 1)
        data.user_name = it
        data.source = 'wechat'
        data.add_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        KeywordsOperate.add_one(data)

# crawl_page('北京')
