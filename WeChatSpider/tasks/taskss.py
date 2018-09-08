#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/5 15:55
@Description: 
"""
from celery import Celery
from .workers import app


@app.task
def add(x, y):
    print("running...", x, y)
    return x + y