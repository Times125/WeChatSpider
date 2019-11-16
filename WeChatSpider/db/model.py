#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/10 8:08
@Description: 
"""
import json
from .basic import Base
from .tables import (search_keyword, weixin_article_data, weixin_account_data,
                     user_monitor_account, crawler_status)
from ..config import (db_charset, db_engine)

__all__ = ['SearchKeyword', 'WeChatArticleData', 'WeChatAccountData',
           'UserMonitorAccount', 'SpiderStatus']


class BaseInfo:
    __table_args__ = {
        'mysql_charset': db_charset,
        'mysql_engine': db_engine,
    }


class SearchKeyword(Base, BaseInfo):
    __table__ = search_keyword


class WeChatArticleData(Base, BaseInfo):
    __table__ = weixin_article_data


class WeChatAccountData(Base, BaseInfo):
    __table__ = weixin_account_data


class UserMonitorAccount(Base, BaseInfo):
    __table__ = user_monitor_account


class SpiderStatus(Base, BaseInfo):
    __table__ = crawler_status
