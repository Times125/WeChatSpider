#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/20 16:58
@Description: 
"""
import time
import re
import json
import math
from bs4 import BeautifulSoup
from ..decorators import parse_decorator

__all__ = ['parse_search_article_result', 'parse_total_page', 'parse_article_content', 'parse_fulltext_url',
           'parse_search_gzh_result',
           'parse_history_url_list']

sogou_domain = 'http://weixin.sogou.com'


@parse_decorator('')
def parse_fulltext_url(html):
    """
    获取全文链接
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, 'html.parser')
    fulltext_url = soup.find('a', attrs={'id': 'js_share_source'}).get('href')
    return fulltext_url


@parse_decorator({'content': '', 'image_list': '', 'page_source': '', 'video': ''})
def parse_article_content(html):
    """
    解析文章内容，包括文字、图片,视频信息
    :param html:
    :return:
    """
    con = dict()
    video = list()
    img_list = list()
    # TODO 抓取文章中的视频信息，如果存在
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find('div', attrs={'id': 'js_article'})
    if content:
        content = content.get_text()  # 文章文字内容
        con['content'] = content if content else ''
    else:
        con['content'] = ''
    pngs = soup.find_all('img', attrs={'data-type': 'png'})
    if not pngs:
        pngs = list()

    jpgs = soup.find_all('img', attrs={'data-type': 'jpeg'})
    if not jpgs:
        jpgs = list()

    if pngs or jpgs:
        pngs.extend(jpgs)  # 文章包含的图片
        for png in pngs:
            img_list.append(png.get('data-src'))
    con['image_list'] = ','.join(img_list) if img_list else ''

    page_source = soup.find('div', attrs={'id': 'js_article'})

    if page_source:
        page_source = str(page_source).replace('data-src', 'src')  # 包含标签的文章内容，用于源文章呈现
        con['page_source'] = page_source if page_source else ''
    else:
        con['page_source'] = ''

    con['video'] = ','.join(video) if video else ''

    return con


@parse_decorator(list())
def parse_search_article_result(html):
    """
    解析一页搜索结果中所有的微信文章条目，包括文章标题、摘要、时间、文章来源
    :param html:
    :return:list
    """
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find('ul', attrs={'class': 'news-list'})
    res = list()
    for li in ul.find_all('li'):
        item = dict()
        txt_box = li.find('div', attrs={'class': 'txt-box'})
        article_url = txt_box.find('a').get('href')  # 文章url

        item['article_url'] = article_url if article_url else ""

        article_title = txt_box.find('a').get_text()  # 文章标题
        item['article_title'] = article_title if article_title else ''

        article_abstract = txt_box.find('p', attrs={'class': 'txt-info'}).get_text()  # 文章摘要
        item['article_abstract'] = article_abstract if article_abstract else ''

        article_from = txt_box.find('a', attrs={'class': 'account'}).get_text()  # 文章来源（公众号）
        item['article_from'] = article_from if article_from else ''

        a_time = txt_box.find('div', attrs={'class': 's-p'}).get('t')
        item['article_time'] = int(a_time) * 1000  # 发布时间
        res.append(item)
    return res


@parse_decorator(1)
def parse_total_page(html):
    """
    获取此关键字搜索结果包含的页面数量
    :param html:
    :return: int
    """
    soup = BeautifulSoup(html, 'html.parser')
    res = soup.find('div', attrs={'class': 'mun'}).get_text()
    num = re.findall('(\d+)', res)
    if num:
        num = int(''.join(num))
    if num > 1000:
        num = 1000
    return math.ceil(num / 10)


@parse_decorator(list())
def parse_search_gzh_result(html):
    """
    解析公众号搜索结果页，包括公众号名称，公众号url
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find('ul', attrs={'class': 'news-list2'})
    res = list()
    for li in ul.find_all('li'):
        item = dict()
        txt_box = li.find('div', attrs={'class': 'txt-box'})
        article_url = txt_box.find('a').get('href')  # 公众号url
        item['gzh_url'] = article_url

        article_title = txt_box.find('a').get_text()  # 公众号标题
        item['gzh_name'] = article_title

        res.append(item)
    return res


@parse_decorator(list())
def parse_history_url_list(html):
    """
    获取公众号页面10条历史消息的url
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, 'html.parser')
    base_url = 'https://mp.weixin.qq.com'
    pattern = re.compile(r"var\s*msgList\s*=\s*(.*?);\s*seajs\.use", re.MULTILINE | re.DOTALL)
    real_content = re.search(pattern, html)
    history_json = json.loads(real_content.group(1))
    res = list()
    for info in history_json['list']:
        try:
            item = dict()
            item['article_from'] = soup.title.string

            time_stamp = info['comm_msg_info']['datetime']
            item['article_time'] = time_stamp * 1000

            title = info['app_msg_ext_info']['title']
            item['article_title'] = title

            abstract = info['app_msg_ext_info']['digest']
            item['article_abstract'] = abstract

            if 'multi_app_msg_item_list' in info['app_msg_ext_info']:
                for sub_info in info['app_msg_ext_info']['multi_app_msg_item_list']:
                    sub_item = dict()
                    sub_item['article_from'] = soup.title.string
                    sub_item['article_time'] = time_stamp * 1000
                    sub_item['article_title'] = sub_info['title']
                    sub_item['article_abstract'] = sub_info['digest']
                    content_url = sub_info['content_url']
                    if content_url:
                        if "mp.weixin.qq.com" in content_url:
                            sub_item['article_url'] = content_url.replace('&amp;', "&")
                        else:
                            sub_item['article_url'] = base_url + content_url.replace('&amp;', "&")
                    else:
                        continue
                    res.append(sub_item)

            content_url = info['app_msg_ext_info']['content_url']
            if content_url:
                if "mp.weixin.qq.com" in content_url:
                    item['article_url'] = content_url.replace('&amp;', "&")
                else:
                    item['article_url'] = base_url + content_url.replace('&amp;', "&")
            else:
                continue
            res.append(item)
        except KeyError:
            continue
    return res
