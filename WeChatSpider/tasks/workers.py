#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/5 11:15
@Description: 
"""
from celery import (Celery, platforms)
from WeChatSpider.config import (CeleryConfig, redis_host,
                                 redis_port, redis_pwd,
                                 broker_db, backend_db)

tasks = ['WeChatSpider.tasks.test', ]

platforms.C_FORCE_ROOT = True  # root用户启动celery

# redis://:password@hostname:port/db_number
_broker_url = 'redis://:{}@{}:{}/{}'.format(redis_pwd, redis_host, redis_port, broker_db)
_backend_url = 'redis://:{}@{}:{}/{}'.format(redis_pwd, redis_host, redis_port, backend_db)

app = Celery('WeChatSpider', include=tasks, broker=_broker_url, backend=_backend_url)
app.config_from_object(CeleryConfig)
