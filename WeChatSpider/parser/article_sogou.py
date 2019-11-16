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
           'parse_search_gzh_result', 'parse_gzh_info',
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
    content = soup.find('div', attrs={'id': 'js_content'})  # js_article
    if content:
        content = content.get_text()  # 文章文字内容
        content = re.sub(r'\n{2,*}', '\n', content)
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

        article_title = txt_box.find('a')  # 文章标题
        item['article_title'] = article_title.get_text() if article_title else ''

        article_abstract = txt_box.find('p', attrs={'class': 'txt-info'})  # 文章摘要
        item['article_abstract'] = article_abstract.get_text() if article_abstract else ''

        article_from = txt_box.find('a', attrs={'class': 'account'})  # 文章来源（公众号）
        item['article_from'] = article_from.get_text() if article_from else ''

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


@parse_decorator({'gzh_name': '', 'gzh_id': '', 'gzh_intro': '', 'gzh_firm': '', 'gzh_head_image': ''})
def parse_gzh_info(html):
    """
    解析公众号简介页面
    """
    item = dict()
    soup = BeautifulSoup(html, 'html.parser')
    head_image = soup.find('span', attrs={'class', 'radius_avatar profile_avatar'}).find('img').get('src')
    item['gzh_head_image'] = head_image if head_image else ''

    gzh_name = soup.find('strong', attrs={'class': 'profile_nickname'})
    item['gzh_name'] = gzh_name.get_text().replace('\n', '').strip() if gzh_name else ''

    gzh_id = soup.find('p', attrs={'class': 'profile_account'})  # 微信号
    item['gzh_id'] = gzh_id.get_text().split(':')[-1].strip() if gzh_id else ''

    li_list = soup.find('ul', attrs={'class': 'profile_desc'}).find_all('li')

    gzh_intro = li_list[0].find('div', attrs={'class', 'profile_desc_value'})  # 公众号简介
    item['gzh_intro'] = gzh_intro.get_text() if gzh_intro else ''

    gzh_firm = li_list[1].find('div', attrs={'class', 'profile_desc_value'})  # 公众号主体
    item['gzh_firm'] = gzh_firm.get_text() if gzh_firm else ''

    return item


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
        gzh_url = txt_box.find('a').get('href')  # 公众号url
        item['gzh_url'] = gzh_url if gzh_url else ''

        gzh_name = txt_box.find('a')  # 公众号名称
        item['article_from'] = gzh_name.get_text() if gzh_name else ''

        gzh_id = txt_box.find('label', attrs={'name': 'em_weixinhao'})  # 微信号
        item['gzh_id'] = gzh_id.get_text().split(':')[-1].strip() if gzh_id else ''

        dl_list = li.find_all('dl')
        if len(dl_list) == 3:
            gzh_latest_article = dl_list[2].find('dd').find('a').get('href')  # 最近文章url
            item['article_url'] = gzh_latest_article

            gzh_latest_article = dl_list[2].find('dd').find('a')  # 最近文章title
            item['article_abstract'] = item[
                'article_title'] = gzh_latest_article.get_text() if gzh_latest_article else ''

            publish_time = dl_list[2].find('dd').find('span').find('script').get_text()  # 最近的文章发布时间
            publish_time = re.compile(r'[\d]+').findall(publish_time)[0]
            item['article_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(publish_time)))

        elif len(dl_list) == 2:
            gzh_latest_article = dl_list[1].find('dd').find('a').get('href')  # 最近文章url
            item['article_url'] = gzh_latest_article

            gzh_latest_article = dl_list[1].find('dd').find('a')  # 最近文章title
            item['article_abstract'] = item[
                'article_title'] = gzh_latest_article.get_text() if gzh_latest_article else ''

            publish_time = dl_list[1].find('dd').find('span').find('script').get_text()  # 最近的文章发布时间
            publish_time = re.compile(r'[\d]+').findall(publish_time)[0]
            item['article_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(publish_time)))

        elif len(dl_list) == 1:
            item['article_url'] = ""
            item['article_abstract'] = item['article_title'] = ''
            item['article_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        res.append(item)
    return res
