#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/20 18:02
@Description: 
"""
import time
import requests
import json
from ..parser import is_404
from ..exceptions import SpiderBanError
from ..decorators import timeout_decorator
from ..utils import identify_captcha_callback,identify_captcha_by_human
from ..logger import download_logger
from ..cookies import suv_gen
from ..config import (identify_captcha_retries, identify_sleep_time,
                      headers, request_retries)


@timeout_decorator
def get_page(url, cookies=None, refer=dict()):
    download_logger.info("crawl {} ".format(url))
    print("crawl {} ".format(url))
    refer.update(headers)
    count = 0
    while count < request_retries:
        resp = requests.get(url, headers=refer, cookies=cookies)
        text = resp.text.encode('utf-8').decode('utf-8')
        if 'antispider' in resp.url and '请输入验证码' in text:
            print("=======> 要输入验证码啦")
            cookies = _unlock(url, cookies)
            if not isinstance(cookies, dict):
                raise SpiderBanError("spider has been banned and update cookies failed")
            count += 1
            continue
        if is_404(text):
            return ''
        return text
    return ''


# 解封后返回更新cookies
def _unlock(url, old_cookies, identify_captcha_func=identify_captcha_by_human):
    """
    :param identify_captcha_func: func to identify image
    :param url: the url before captcha occur
    :param old_cookies: requests session object
    :return: the update cookies
    """
    unlock_url = "http://weixin.sogou.com/antispider/thank.php"
    url_suffix = url.split('/')[-1]
    cur_time = 0
    new_cookies = dict()
    captcha = "1A2B3C"
    left_time = identify_captcha_retries
    while cur_time < left_time:
        tc = int(round(time.time()))
        image_content = requests.get('http://weixin.sogou.com/antispider/util/seccode.php?tc={}'.format(tc),
                                     cookies=old_cookies)
        if image_content.ok:
            captcha = identify_captcha_func(image_content)
        data = {
            'c': captcha,
            'r': '%2F' + url_suffix,
            'v': 5}
        headers_new = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://weixin.sogou.com/antispider/?from=%2F{}'.format(url_suffix)
        }

        headers_new.update(headers)
        unlock_resp = requests.post(unlock_url, data, headers=headers_new, cookies=old_cookies)
        resp = json.loads(unlock_resp.text, encoding='utf-8')
        # {"code": 0,"msg": "解封成功，正在为您跳转来源地址...", "id": "790884BFC2C4B78EC440C7ACC232798B"}
        # {"code": 3,"msg": "验证码输入错误, 请重新输入！"}
        if resp.get('code') != 0:
            print('验证码输入错误')
            cur_time += 1
            time.sleep(identify_sleep_time)
            continue
        new_cookies['SNUID'] = resp.get('id')
        new_cookies['SUV'] = suv_gen()
        return new_cookies

    return ''
