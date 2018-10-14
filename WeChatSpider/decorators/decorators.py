#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/8/28 19:45
@Description: 
"""
from functools import wraps
from WeChatSpider.logger import (download_logger, parse_logger)
from traceback import format_tb
from requests.exceptions import (Timeout, ConnectTimeout,
                                 ReadTimeout, ConnectionError)

__all__ = ['timeout_decorator', 'parse_decorator']


def timeout_decorator(func):
    @wraps(func)
    def time_limit(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (Timeout, ConnectTimeout, ReadTimeout, ConnectionError) as e:
            download_logger.error("Exception '{}' occurred when crawl url '{}', traceback: {}".format(e, args[0],
                                                                                                      format_tb(
                                                                                                          e.__traceback__)))
            return ""

    return time_limit


def parse_decorator(value):
    """
    :param value: the default value when exceptions happened
    :return: any value you want, like 0,'',[] or None
    """

    def parse_page(func):
        @wraps(func)
        def handle_error(*args):
            try:
                return func(*args)
            except Exception as e:
                parse_logger.error(
                    "Exception '{}' occurred when parse page, traceback: {}".format(e, format_tb(e.__traceback__)))
                return value

        return handle_error

    return parse_page
