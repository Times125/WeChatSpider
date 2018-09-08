#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/4 16:49
@Description: celery setting
"""


class CeleryConfig:
    enable_utc = False
    timezone = 'Asia/Shanghai'
    accept_content = ['json']
    task_serializer = 'json'
    result_serializer = 'json'
    """
    - 定义了一个worker在消息(任务)被安排给另一个worker之前的等待时间.
    - 可能存在的问题:当broker使用redis时,如果ETA时间长于任务的可见时间,会导致任务重复执行.
    - 有两个解决办法:1.visibility_timeout 设置的尽可能大;2.broker使用rabbitmq;但方案1并不是一个最优解决方案,
    - 详细可以阅读: 
    - https://github.com/celery/celery/issues/4400
    - https://github.com/celery/celery/issues/3270
    - https://github.com/cameronmaske/celery-once
    """
    broker_transport_options = {'visibility_timeout': 60 * 60 * 6}  # 6 hours
    # I/O-bound,选择cpu核心×2的并发比较适宜;CPU-bound,设置为cpu核心数为宜
    worker_concurrency = 4 * 2
    # worker存活时间:在执行120次任务后,此worker被回收,可以防止内存泄露
    worker_max_tasks_per_child = 120
    # 任务队列
    task_queues = {
        'test': {
            'exchange': 'test',  # 交换机名字为test
            'exchange_type': 'topic',  # 交换机类型topic、fanout、direct
            'routing_key': 'test.*'  # 路由键
        },
    }

    # 任务路由,将任务消息发往指定的队列,凡是被@app.task装饰的任务都需要指定任务路由
    task_routes = {
        'WeChatSpider.tasks.test.execute_add': {
            'queue': 'test',  # 队列名
            'routing_key': 'test.add'  # 路由键
        },
        'WeChatSpider.tasks.test.add': {
            'queue': 'test',  # 队列名
            'routing_key': 'test.add'  # 路由键
        },
    }

    # 设置定时周期
    beat_schedule = {
        'test': {
            'task': 'WeChatSpider.tasks.test.execute_add',
            'schedule': 60 * 60 * 24,  # 每天执行一次
        },
    }
