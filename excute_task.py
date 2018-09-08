#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/5 14:02
@Description: 执行的任务为周期性任务，周期时间由celery_config 中beat_schedule对应的时间来确定。
"""
import click
from WeChatSpider.tasks import tasks_map
from WeChatSpider.exceptions import NoTaskException
from WeChatSpider.tasks.test import execute_add


@click.command()
@click.option('--task', type=click.Choice(tasks_map.keys()))
def execute_task(task):
    print(task)
    if not task:
        raise NoTaskException('You have not assigned any task,please check!')
    schedule = tasks_map.get(task)
    schedule()


if __name__ == '__main__':
    """
    first run "celery -A WeChatSpider.tasks.workers worker" in cmd;
    then run "celery beat -A WeChatSpider.tasks.workers worker" in cmd;
    finally run with parameters,use like "python execute_task.py --task test",'test' is one of tasks
    """
    # execute_task()
    execute_add()
