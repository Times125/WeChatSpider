#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/10/13 13:18
@Description: 
"""
from WeChatSpider.tasks import crawl_page


class TestArticle(object):
    def test_crawl_page(self):
        crawl_page("北京")
