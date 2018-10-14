#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/20 16:58
@Description: 
"""
import re
import time
import math
from bs4 import BeautifulSoup
from ..decorators import parse_decorator

__all__ = ['get_data', 'get_total_page', 'get_article_content', 'get_fulltext_url']


@parse_decorator('')
def get_fulltext_url(html):
    """
    获取全文链接
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, 'html.parser')
    fulltext_url = soup.find('a', attrs={'id': 'js_share_source'}).get('href')
    return fulltext_url


@parse_decorator(dict())
def get_article_content(html):
    """
    解析文章内容，包括文字、图片,视频信息
    :param html:
    :return:
    """
    con = dict()
    video = list()
    # TODO 抓取文章中的视频信息，如果存在
    soup = BeautifulSoup(html, 'html.parser')
    page_source = str(soup.find('div', attrs={'id': 'js_article'})).replace('data-src', 'src')  # 包含标签的文章内容，用于源文章呈现
    content = soup.find('div', attrs={'id': 'js_article'}).get_text()  # 文章文字内容
    pngs = soup.find_all('img', attrs={'data-type': 'png'})
    jpgs = soup.find_all('img', attrs={'data-type': 'jpeg'})
    pngs.extend(jpgs)  # 文章包含的图片
    img_list = list()
    for png in pngs:
        img_list.append(png.get('data-src'))
    con['content'] = content if content else ''
    con['image_list'] = ','.join(img_list) if img_list else ''
    con['page_source'] = page_source if page_source else ''
    con['video'] = ','.join(video) if video else ''
    return con


@parse_decorator(dict())
def get_data(html):
    """
    解析一页搜索结果中所有的微信文章条目，包括文章标题、摘要、时间、文章来源
    :param html:
    :return:dict
    """
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find('ul', attrs={'class': 'news-list'})
    res = list()
    for li in ul.find_all('li'):
        item = dict()
        txt_box = li.find('div', attrs={'class': 'txt-box'})
        article_url = txt_box.find('a').get('href')  # 文章url
        item['article_url'] = article_url if article_url else ''

        article_title = txt_box.find('a').get_text()  # 文章标题
        item['article_title'] = article_title if article_title else ''

        article_abstract = txt_box.find('p', attrs={'class': 'txt-info'}).get_text()  # 文章摘要
        item['article_abstract'] = article_abstract if article_abstract else ''

        article_from = txt_box.find('a', attrs={'class': 'account'}).get_text()  # 文章来源（公众号）
        item['article_from'] = article_from if article_from else ''

        a_time = txt_box.find('div', attrs={'class': 's-p'}).find('span', attrs={'class': 's2'}).get_text()
        a_time = re.findall('(\d+)', a_time if a_time else '31507200')[0]  # default time 1971.01.01
        article_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(a_time)))  # 发布时间
        item['article_time'] = article_time

        res.append(item)
    return res


@parse_decorator(1)
def get_total_page(html):
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
