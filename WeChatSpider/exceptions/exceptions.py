#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/8/28 19:18
@Description: 
"""
__all__ = ["Timeout", "NoCookiesException", "VerificationCodeError",
           "OverrideAttrException", "NoTaskException", "SpiderBanError"]


class Timeout(Exception):
    """
    Functions run out of time
    """


class NoCookiesException(Exception):
    """
    Has no cookies in redis
    """


class VerificationCodeError(Exception):
    """
    Verification Codes identify error
    """


class OverrideAttrException(Exception):
    """
    Override class attributions exception
    """


class NoTaskException(Exception):
    """
    No task to access exception
    """


class SpiderBanError(Exception):
    """
    spider has been banned
    """
