#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/4 20:11
@Description: 
"""
import time
from celery import group
from .workers import app


@app.task
def add(a, b):
    res = a + b
    # with open('test.txt', 'a+', encoding='utf-8') as w:
    #     w.write(str(res) + "\n")
    print('sleeping now....', app.current_task)
    time.sleep(11 * 60)
    return res


@app.task
def execute_add():
    # print(app.conf)
    # wait = [(1, 1), (1, 2), (1, 3)]
    wait = [1, ]
    # from datetime import datetime, timedelta
    # tomorrow = datetime.utcnow() + timedelta(seconds=10 * 60)
    # add.apply_async((1, 1), eta=tomorrow)

    # caller = group(add(a, b) for a, b in wait)
    caller = group(add.s(b, 1) for b in wait)
    caller.delay()
    # print('execute_add...')
