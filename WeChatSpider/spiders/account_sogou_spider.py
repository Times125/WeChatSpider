#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/09/08 18:43
@Description: 基于微信搜狗的持续抓取指定公众号发布文章;这里需要注意有两种不同的验证码模式
"""
import time

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


def search_article_by_account(account_object):
    """
    根据账号的执行抓取任务
    :param account_object:
    :return:
    """
    if account_object:
        wechat_api = WechatAPI()
        print(account_object.add_time)
        # wechat_api.crawl(account_object.user_name, SearchType.gzh_account)
    else:
        return ''  # if expire, do nothing, just return


def execute_monitor_account_task():
    """
    任务入口，获取被监控微信公众号列表，然后执行监视任务
    :return:
    """
    while True:
        account_lists = KeywordsOperate.get_user_monitor_accounts()
        # 网络错误或者数据库错误
        if not account_lists:
            db_logger.error('网络错误或者数据库故障导致无可监控微信公众号！请检查是否有可用公众号')
            SpiderStatusDao.save_spider_status('网络错误或者数据库故障导致无可监控微信公众号！请检查是否有可用公众号', 0)
            time.sleep(300)
            continue
        for idx, item in enumerate(account_lists):
            search_article_by_account(item)

        SpiderStatusDao.save_spider_status('', 1)
        time.sleep(update_internal)
