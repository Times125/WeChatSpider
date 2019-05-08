#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/11/17 16:17
@Description: 
"""
from kafka import (SimpleProducer, SimpleClient)
from kafka.errors import KafkaUnavailableError, FailedPayloadsError

from ..db import SpiderStatusDao
from ..config import (kafka_server, kafka_topics)
from ..logger import other_logger

__all__ = ['write2kafka']

client = SimpleClient(kafka_server)

try:
    producer = SimpleProducer(client)
except KafkaUnavailableError as e:
    other_logger.error('get kafka producer error,look: {}'.format(e))
    SpiderStatusDao.save_spider_status('获取kafka消费者失败！{}'.format(e))


def write2kafka(data):
    for topic in kafka_topics:
        try:
            producer.send_messages(topic, str.encode(data))
            print('send message success!')
        except FailedPayloadsError as e:
            other_logger.error('send message error,look: {}'.format(e))
            write2kafka_again(data)
            SpiderStatusDao.save_spider_status('数据写入kafka失败！')


def write2kafka_again(data):
    for topic in kafka_topics:
        try:
            producer.send_messages(topic, str.encode(data))
            print('send message again success!')
        except FailedPayloadsError as e:
            other_logger.error('send message error,look: {}'.format(e))
            SpiderStatusDao.save_spider_status('数据写入kafka失败！')
