#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/10 8:08
@Description: 
"""
from sqlalchemy import Table, Column, INTEGER, String, Text
from sqlalchemy.dialects.mysql import LONGTEXT, BIGINT, DATETIME, VARCHAR
from .basic import metadata

# 关键词种子
search_keyword = Table('search_keyword', metadata,
                       Column('id', INTEGER, primary_key=True, autoincrement=True),
                       Column('keyword', String(128), unique=True),
                       Column('add_time', DATETIME),  # 关键词添加时间
                       )

# 抓取的文章内容
weixin_article_data = Table('weixin_article_data', metadata,
                            Column('id', INTEGER, primary_key=True, autoincrement=True),
                            Column('url', String(1024), server_default=''),  # 文章链接
                            Column('title', String(1024), server_default=''),  # 文章标题
                            Column('content', Text),  # 文章内容
                            Column('source', String(128), server_default=''),  # 文章来源
                            Column('publish_time', DATETIME),  # 文章发表日期
                            Column('video', Text),  # 文章视频
                            Column('abstract', String(1024), server_default=''),  # 文章摘要
                            Column('image_urls', Text),  # 内嵌图片链接
                            Column('fetch_time', DATETIME),  # 文章抓取时间
                            Column('search_word', String(50)),  # 搜索的关键字
                            )

# 公众号信息
weixin_account_data = Table('weixin_account_data', metadata,
                            Column('id', INTEGER, primary_key=True, autoincrement=True),
                            Column('weixin_id', String(128), server_default=''),  # 微信号
                            Column('weixin_name', String(128), server_default=''),  # 微信名称
                            Column('weixin_intro', String(1024)),  # 功能介绍
                            Column('weixin_firm', String(512)),  # 微信主体
                            Column('head_image', Text),  # 头像的 url
                            Column('fetch_time', DATETIME),  # 抓取时间
                            )

# 被监控的公众号表
user_monitor_account = Table('user_monitor_account', metadata,
                             Column('id', INTEGER, primary_key=True, autoincrement=True),
                             Column('url', String(500), unique=True),  # 公众号首页地址
                             Column('user_name', String(500), ),  # 要搜索的公众号名
                             Column('source', String(128)),  # 监控表来源
                             Column('add_time', DATETIME),  # 添加时间
                             )

# 用于更新爬虫状态
crawler_status = Table('crawler_status', metadata,
                       Column('id', INTEGER, primary_key=True, autoincrement=True),
                       Column('name', String(100), unique=True),
                       Column('update_time', BIGINT),
                       Column('status', INTEGER, default=1),
                       Column('exception', String(500)),
                       Column('crawl_interval', INTEGER),
                       Column('real_crawl_interval', INTEGER),
                       Column('mail', String(100)),
                       )
