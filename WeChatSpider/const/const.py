#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/8/28 21:06
@Description: 
"""
from WeChatSpider.exceptions import OverrideAttrException
from functools import wraps

__all__ = ["SearchType",]


def Const(cls):
    @wraps(cls)
    def new_setattr(self, name, value):
        raise OverrideAttrException('constant : {} can not be changed'.format(name))

    cls.__setattr__ = new_setattr
    return cls


@Const
class SearchType(object):
    gzh_account = 1  # 表示搜公众号
    article = 2  # 表示搜文章