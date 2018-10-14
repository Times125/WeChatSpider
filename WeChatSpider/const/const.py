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
    offical_account = 1  # 表示搜公众号
    article = 2  # 表示搜文章

# @Constant
# class _SearchArticleTypeConst(object):
#     all = 'all'
#     rich = 'rich'
#     video = 'video'
#     image = 'image'
#
#
# @Constant
# class _SearchArticleTimeConst(object):
#     """搜索条件 时间
#
#     0 没有限制 / 1一天 / 2一周 / 3一月 / 4一年 / 5自定
#     """
#     anytime = 0
#     day = 1
#     week = 2
#     month = 3
#     year = 4
#     specific = 5
#
#
# @Constant
# class _Const(object):
#     search_article_type = _SearchArticleTypeConst()
#     search_article_time = _SearchArticleTimeConst()
#
#
# WechatSogouConst = _Const()
