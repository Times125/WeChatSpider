#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/10/12 23:01
@Description: 
"""
from ..decorators import parse_decorator

__all__ = ['is_404', ]


@parse_decorator(False)
def is_404(html):
    # 需要登录才能抓10页以后的数据
    if 'b404-box' in html:
        return True
    return False
