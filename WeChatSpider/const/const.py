#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/8/28 21:06
@Description: 
"""
from WeChatSpider.exceptions import OverrideAttrException
from functools import wraps


def Constant(cls):
    @wraps(cls)
    def new_setattr(self, name, value):
        raise OverrideAttrException('constant : {} can not be changed'.format(name))

    cls.__setattr__ = new_setattr
    return cls


@Constant
class A(object):
    a = 1
