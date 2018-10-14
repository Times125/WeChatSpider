#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/10 8:08
@Description: 
"""
from sqlalchemy import Table, Column, INTEGER, String, Text
from .basic import metadata

weixin_seeds = Table('weixin_seeds', metadata,
                     Column('id', INTEGER, primary_key=True, autoincrement=True),
                     Column('keyword', String(128), unique=True),
                     Column('type', String(20), server_default='article'),
                     Column('date', String(1024), server_default=''),
                     Column('expire', String(1024), server_default=''),  # 关键词生命周期
                     )

weixin_article = Table('weixin_article', metadata,
                       Column('id', INTEGER, primary_key=True, autoincrement=True),
                       Column('title', String(1024), server_default=''),  # 文章标题
                       Column('account', String(128), server_default=''),  # 文章来源
                       Column('date', String(128), server_default=''),  # 文章发表日期
                       Column('url', String(1024), server_default=''),  # 文章链接
                       Column('video', Text),  # 文章视频
                       Column('abstract', String(1024), server_default=''),  # 文章摘要
                       Column('image_urls', Text),  # 文章摘要
                       Column('content', Text),  # 文章内容
                       Column('source', Text),  # 文章带标签的内容，用于展示
                       )
