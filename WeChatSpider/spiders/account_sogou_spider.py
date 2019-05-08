#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/09/08 18:43
@Description: 基于微信搜狗的持续抓取指定公众号发布文章;这里需要注意有两种不同的验证码模式
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


# def crawl_content(article_list, refer, name):
#     """
#     根据文章列表，抓取具体每个文章的详细内容
#     :param article_list:
#     :param refer:
#     :param name:
#     :return:
#     """
#     if not article_list:
#         return ''
#     # article_datas = list()
#     for item in article_list:
#         wx_article = WeiChatArticleData()
#         if bloomfilter.is_exists(item['article_title'] + str(item['article_time'])):  # 以文章名和文章发布时间来衡量是否重复抓取
#             continue
#         if not item['article_url']:
#             continue
#         html = get_article_page(item['article_url'], refer)
#         if not html:
#             # print("crawl content failed, the url is {}".format(item['article_url']))
#             download_logger.warning("crawl content failed, the url is {}".format(item['article_url']))
#             continue
#         # 当出现转发，需要点阅读全文的时候，得重新获取链接加载
#         if '阅读全文' in html or 'js_share_source' in html:
#             fulltext_url = parse_fulltext_url(html)
#             if not fulltext_url:
#                 continue
#             html = get_article_page(fulltext_url, refer)
#             if not html:
#                 continue
#         content_dict = parse_article_content(html)
#         wx_article.url = item['article_url']
#         wx_article.title = item['article_title']
#         wx_article.source = name
#         wx_article.publish_time = item['article_time']
#         wx_article.abstract = item['article_abstract']
#         wx_article.content = content_dict['content']
#         wx_article.image_urls = content_dict['image_list']
#         wx_article.video = content_dict['video']
#         wx_article.raw_content = content_dict['page_source']
#         wx_article.fetch_time = int(time.time() * 1000)
#         wx_article.search_word = name
#         wx_article.md5 = md5(item['article_title'] + str(item['article_time']))
#         # article_datas.append(wx_article)
#         write2kafka(wx_article.to_json())  # 往kafka中写，不写mysql了
#         # 更新缓存中间表
#         _cache = CacheMidTable()
#         _cache.url = wx_article.url
#         _cache.md5 = wx_article.md5
#         _cache.proxy = 0
#         CacheDataDao.save(_cache)
#         time.sleep(2)
#     # CommonOperate.add_all(article_datas)


def search_article_by_account(account_object):
    """
    根据账号的执行抓取任务
    :param account_object:
    :return:
    """
    if account_object:
        wechat_api = WechatAPI()
        wechat_api.crawl(account_object.user_name, SearchType.gzh_account)
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
