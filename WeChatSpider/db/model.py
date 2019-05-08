#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/10 8:08
@Description: 
"""
import json
from .basic import Base
from .tables import (search_keyword, weixin_article_data,
                     user_monitor_account, cache_mid_table,
                     crawler_status)

__all__ = ['SearchKeyword', 'WeiChatArticleData',
           'UserMonitorAccount', 'CacheMidTable', 'SpiderStatus']


class SearchKeyword(Base):
    __table__ = search_keyword


class WeiChatArticleData(Base):
    __table__ = weixin_article_data


class UserMonitorAccount(Base):
    __table__ = user_monitor_account


class CacheMidTable(Base):
    __table__ = cache_mid_table


class SpiderStatus(Base):
    __table__ = crawler_status


def to_dict(self):
    ignore_name = ['id']
    data = {c.name: getattr(self, c.name, None) for c in self.__table__.columns if c.name not in ignore_name}
    data['table'] = self.__table__.name
    return data


def to_json(self):
    data = to_dict(self)
    return json.dumps(data)


# monkey patch：热插件补丁
Base.to_dict = to_dict
Base.to_json = to_json
