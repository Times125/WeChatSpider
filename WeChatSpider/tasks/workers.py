#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/5 11:15
@Description: 
"""
from celery import (Celery, platforms)
from WeChatSpider.config import (CeleryConfig, REDIS_HOST,
                                 REDIS_PORT, REDIS_PASSWORD,
                                 BROKER_DB, BACKEND_DB)

tasks = ['WeChatSpider.tasks.test', ]

platforms.C_FORCE_ROOT = True  # root用户启动celery

# redis://:password@hostname:port/db_number
_broker_url = 'redis://:{}@{}:{}/{}'.format(REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, BROKER_DB)
_backend_url = 'redis://:{}@{}:{}/{}'.format(REDIS_PASSWORD, REDIS_HOST, REDIS_PORT, BACKEND_DB)

app = Celery('WeChatSpider', include=tasks, broker=_broker_url, backend=_backend_url)
app.config_from_object(CeleryConfig)
