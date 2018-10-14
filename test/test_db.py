#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/10 21:39
@Description: 
"""
import pytest
from datetime import datetime, timedelta
from WeChatSpider.db import (WeiChatSeeds, CommonOperate, KeywordsOperate)
from WeChatSpider.utils import (identify_captcha_by_human, )


class TestDatabase(object):

    def test_add_one(self):
        co = CommonOperate()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        expire = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        seed_data = WeiChatSeeds(keyword="川大", type="article", date=date, expire=expire)
        co.add_one(seed_data)

    def test_add_all(self):
        co = CommonOperate()
        seed_datas = list()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        expire = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        keywords = ['北大', '清华', '复旦', '浙大', '上交']
        for i in range(5):
            seed_datas.append(WeiChatSeeds(keyword=keywords[i], type="article", date=date, expire=expire))
        co.add_all(seed_datas)

    def test_get_entities_by_key(self):
        co = CommonOperate()
        res = co.get_entities_by_key(WeiChatSeeds, ['id', 'keyword', 'type', 'date', 'expire'])
        print(res)

    def test_get_entity_by_key(self):
        co = CommonOperate()
        res = co.get_entity_by_key(WeiChatSeeds, 'id={}'.format(1))
        print('res=', res.date)

    def test_get_search_keywords(self):
        ko = KeywordsOperate()
        res = ko.get_search_keywords()
        print(res)


class TestUtils(object):
    def test_identify_captcha_by_human(self):
        with open('../image_dir/2a2j.jpg', 'rb') as r:
            image = r.read()
        res = identify_captcha_by_human(image)
        print(res)
