#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/09/08 17:02
@Description: 基于微信搜狗的按关键字搜索文章
"""
import time
from ..const import (
    SearchType
)
from ..downloader import (
    WechatAPI
)
from ..db import (
    KeywordsOperate, SpiderStatusDao
)
from ..config import (
    update_internal
)

from ..logger import (
    db_logger
)

__all__ = ['search_article_by_keyword', 'execute_search_article_task']


def search_article_by_keyword(keyword_object):
    """
    根据关键词执行抓取任务
    :param keyword_object:
    :return:
    """
    if keyword_object:
        wechat_api = WechatAPI()
        wechat_api.crawl(keyword_object.keyword, SearchType.article)
    else:
        return ''  # if expire, do nothing, just return


def execute_search_article_task():
    """
    任务入口，获取关键词表，然后执行抓取任务
    :return:
    """
    while True:
        keyword_objects = KeywordsOperate.get_search_keywords()
        # 网络错误或者数据库错误
        if not keyword_objects:
            db_logger.error('网络错误或者数据库故障导致无可用关键词！请检查是否有可用搜索关键词')
            SpiderStatusDao.save_spider_status('网络错误或者数据库故障导致无可用关键词！请检查是否有可用搜索关键词', 0)
            time.sleep(300)
            continue
        for idx, item in enumerate(keyword_objects):
            search_article_by_keyword(item)

        # 提交爬虫状态
        SpiderStatusDao.save_spider_status('', 1)
        time.sleep(update_internal)
