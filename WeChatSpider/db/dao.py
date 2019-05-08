#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/10 7:43
@Description: 
"""
import time

from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from sqlalchemy.exc import InvalidRequestError

from WeChatSpider.config import update_internal
from .basic import get_db_session
from ..logger import db_logger
from .model import (SearchKeyword, UserMonitorAccount, SpiderStatus)

__all__ = ['CommonOperate', "KeywordsOperate", 'SpiderStatusDao', 'CacheDataDao']


class CommonOperate:
    @classmethod
    def add_one(cls, data):
        with get_db_session() as db_session:
            try:
                db_session.add(data)
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                db_logger.error("exception '{}' happened when add data".format(e))

    @classmethod
    def add_all(cls, datas):
        with get_db_session() as db_session:
            try:
                db_session.add_all(datas)
                db_session.commit()
            except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError) as e:
                print('error', e)
                db_session.rollback()
                for data in datas:
                    cls.add_one(data)


class KeywordsOperate(CommonOperate):
    @classmethod
    def get_search_keywords(cls):
        rs = None
        with get_db_session() as db_session:
            rs = db_session.query(SearchKeyword).all()
        return rs

    @classmethod
    def get_user_monitor_accounts(cls):
        rs = None
        with get_db_session() as db_session:
            rs = db_session.query(UserMonitorAccount).filter(UserMonitorAccount.source == 'wechat').all()
        return rs


# 更新爬虫状态
class SpiderStatusDao(CommonOperate):
    @classmethod
    def save(cls, status_data):
        rs = 1
        with get_db_session() as db_session:
            try:
                db_session.add(status_data)
                db_session.commit()
            except SqlalchemyIntegrityError:
                db_session.rollback()
                cls.update(status=status_data.status, update_time=status_data.update_time,
                           real_crawl_interval=status_data.real_crawl_interval, exception=status_data.exception)
                rs = 0
            except Exception as e:
                db_logger.error('exception {} is raied'.format(e))
                rs = 0
        return rs

    @classmethod
    def update(cls, name='wechat', **kwargs):
        with get_db_session() as db_session:
            try:
                db_session.query(SpiderStatus).filter(SpiderStatus.name == name).update(kwargs)
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                db_logger.error("update spider's status error, look: {}".format(e))
                db_session.query(SpiderStatus).filter(SpiderStatus.name == name).update({'exception': str(e)[:500]})
                db_session.commit()

    @classmethod
    def save_spider_status(cls, exception=None, stat=1):
        status = SpiderStatus()
        status.name = 'wechat'
        status.update_time = int(time.time() * 1000)
        status.exception = exception
        status.status = stat
        status.real_crawl_interval = update_internal
        SpiderStatusDao.save(status)


class CacheDataDao(CommonOperate):
    @classmethod
    def save(cls, cache_data):
        rs = 1
        with get_db_session() as db_session:
            try:
                db_session.add(cache_data)
                db_session.commit()
            except SqlalchemyIntegrityError:
                db_session.rollback()
                # cls.update(info.post_id, info.keyword, info.last_reply_time)
                rs = 0
            except Exception as e:
                db_logger.error('exception {} is raied'.format(e))
                rs = 0
        return rs
