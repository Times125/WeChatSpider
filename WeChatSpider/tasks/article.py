#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/09/08 17:02
@Description: 按关键字搜索文章
"""
import time
from datetime import datetime
from celery import group
from .workers import app
from ..db import (WeiChatArticle, CommonOperate, KeywordsOperate)
from ..config import (max_search_page, adaptive_page, bloomfilter_article)
from ..cookies import get_cookies
from ..const import SearchType
from ..exceptions import SpiderBanError
from ..downloader import get_page
from ..logger import download_logger
from ..parser import (get_data, get_total_page,
                      get_article_content, get_fulltext_url)
from ..bloomfilter import BloomFilterRedis

__all__ = ['crawl_page', 'crawl_content_by_page', 'search_article_by_keyword', 'execute_search_article_task']

Base_Url = "http://weixin.sogou.com/weixin?type={}&s_from=input&query={}&ie=utf8&page={}"


@app.tasks
def crawl_content(article_list, cookies, refer):
    """
    根据文章列表，抓取具体每个文章的详细内容
    :param article_list:
    :param cookies:
    :param refer:
    :return:
    """
    print("==================>crawl_content()")
    bloomfilter = BloomFilterRedis(key=bloomfilter_article)
    if not article_list:
        return ''
    print('=====>article_list', article_list)
    article_datas = list()
    print(len(article_list), '=============>文章页抓取到这么多')
    for item in article_list:
        wx_article = WeiChatArticle()
        if bloomfilter.is_exists(item['article_from'] + item['article_time']):  # 以公众号名和文章发布时间来衡量是否重复抓取
            print('存在！！！！')
            continue
        html = get_page(item['article_url'], cookies, refer)  # item[0] is article_url
        if not html:
            print("crawl content failed, the url is {}".format(item['article_url']))
            download_logger.warning("crawl content failed, the url is {}".format(item['article_url']))
            continue
        # TODO 当出现转发，需要点阅读全文的时候，得重新获取链接加载
        if '阅读全文' in html and 'js_share_source' in html:
            fulltext_url = get_fulltext_url(html)
            html = get_page(fulltext_url, cookies, refer)
            if not html:
                print("crawl content failed, the url is {}".format(fulltext_url))
                download_logger.warning("crawl content failed, the url is {}".format(fulltext_url))
                wx_article.date = item['article_time']
                wx_article.title = item['article_title']
                wx_article.abstract = item['article_abstract']
                wx_article.account = item['article_from']
                wx_article.url = item['article_url']
                CommonOperate.add_one(wx_article)
                continue
        content_dict = get_article_content(html)
        # [article_url, article_title, article_abstract, article_from, article_time]
        wx_article.date = item['article_time']
        wx_article.title = item['article_title']
        wx_article.abstract = item['article_abstract']
        wx_article.account = item['article_from']
        wx_article.url = item['article_url']
        wx_article.content = content_dict['content']
        wx_article.image_urls = content_dict['image_list']
        wx_article.source = content_dict['page_source']
        wx_article.video = content_dict['video']
        article_datas.append(wx_article)
        print('================>', item['article_from'])
    CommonOperate.add_all(article_datas)


@app.task
def crawl_page(keyword):
    """
    根据关键字抓取搜索结果页
    :param keyword:
    :return:
    """
    cur_page = 1
    wait2crawl_page = max_search_page
    cookies = get_cookies()
    # 一定要加refer
    while cur_page <= wait2crawl_page:
        print("====>抓取第{}页".format(cur_page))
        url = Base_Url.format(SearchType.article, keyword, cur_page)
        refer = Base_Url.format(SearchType.article, keyword, cur_page if cur_page == 1 else cur_page - 1)
        try:
            html = get_page(url, cookies, {'Refer': refer})
        except SpiderBanError as e:
            download_logger.error(e)
            continue
        if html:
            article_list = get_data(html)
            if cur_page == 1:
                if adaptive_page:
                    wait2crawl_page = get_total_page(html)
            crawl_content(article_list, cookies, {'Refer': refer})
            cur_page += 1
        time.sleep(10)
    pass


@app.task
def crawl_content_by_page(page_num):
    pass


@app.task
def search_article_by_keyword(keyword_object):
    expire = datetime.strptime(keyword_object[4], "%Y-%m-%d %H:%M:%S")
    time_now = datetime.now()
    if time_now <= expire:
        crawl_page(keyword_object[1])
    else:
        return ''  # if expire, do nothing, just return


@app.task
def execute_search_article_task():
    keyword_objects = KeywordsOperate.get_search_keywords()
    caller = group(search_article_by_keyword.s(kw_obj) for kw_obj in keyword_objects)
    caller.delay()
