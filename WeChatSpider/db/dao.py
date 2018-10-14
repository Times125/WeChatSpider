#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/10 7:43
@Description: 
"""

from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from sqlalchemy.exc import InvalidRequestError

from .basic import get_db_session
from ..logger import db_logger
from .model import WeiChatSeeds

__all__ = ['CommonOperate', "KeywordsOperate"]


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
                print('error')
                for data in datas:
                    cls.add_one(data)

    @classmethod
    def get_entity_by_key(cls, model, conditions):
        """
        get one entity according filter conditions
        :param model:
        :param conditions: filter conditions
        :return:
        """
        with get_db_session() as db_session:
            return db_session.query(model).filter(text(conditions)).first()

    @classmethod
    def get_entities_by_key(cls, model, attrs, conditions='1'):
        """
        :param model:table model
        :param attrs: table attr list
        :param conditions: filter conditions
        :return: list of entity
        """
        model_attrs = []
        for attr in attrs:
            model_attr = getattr(model, attr)
            if model_attr:
                model_attrs.append(model_attr)
        # print([a.__str__() for a in model_attrs])
        # ['WeiChatSeeds.id', 'WeiChatSeeds.keyword', 'WeiChatSeeds.type', 'WeiChatSeeds.date']
        with get_db_session() as db_session:
            return db_session.query(*model_attrs).filter(text(conditions)).all()

    @classmethod
    def update_insert_entity(cls, model, conditions, attrs_map):
        pass

    @classmethod
    def set_entity_attr(cls, model, conditions, attrs_map):
        pass


class KeywordsOperate(CommonOperate):
    @classmethod
    def get_search_keywords(cls):
        attrs = ['id', 'keyword', 'type', 'date', 'expire']
        return cls.get_entities_by_key(WeiChatSeeds, attrs, conditions='1')
