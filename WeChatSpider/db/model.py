#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/10 8:08
@Description: 
"""
from .basic import Base
from .tables import (weixin_seeds, weixin_article)

__all__ = ['WeiChatSeeds', 'WeiChatArticle']


class WeiChatSeeds(Base):
    __table__ = weixin_seeds


class WeiChatArticle(Base):
    __table__ = weixin_article
