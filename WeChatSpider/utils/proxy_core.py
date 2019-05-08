#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/12/16 21:53
@Description: 
"""
import requests
import json
from WeChatSpider.logger import other_logger

__all__ = ['get_proxy', 'get_proxies', 'refresh_proxy', 'del_proxy']


def get_proxy():
    """
    获取一个代理
    :return:
    """
    try:
        resp = requests.get('http://10.0.12.1:5000/proxy/get/https')  # 获取通过https校验器的单个ip
        if resp.text:
            res = json.loads(resp.text.encode('utf8').decode('utf8'))
            if res['status_code'] == 200:
                proxy = res['proxy']
                return proxy
        return ''
    except TimeoutError as e:
        other_logger.error('get proxy failed,look {}'.format(e))
        return ''


def refresh_proxy():
    """
    刷新代理并返回新的代理
    :return:
    """
    try:
        resp = requests.get('http://10.0.12.1:5000/pool/refresh/https')  # 刷新代理ip
        if resp.text:
            res = json.loads(resp.text.encode('utf8').decode('utf8'))
            if res['status_code'] == 200:
                proxy_pool = res['pool']
                return proxy_pool
        return []
    except TimeoutError as e:
        other_logger.error('get proxy failed,look {}'.format(e))
        return []


def get_proxies(batch_size=10):
    """
    获取批量代理ip,蘑菇代理
    :param batch_size:
    :return:
    """
    try:
        resp = requests.get('http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=45cce39ad9a448e99cdbf0cf821a1fed&'
                            'count={}&expiryDate=0&format=1&newLine=2'.format(batch_size))  # 获取通过https校验器的20个ip
        if resp.text:
            res = json.loads(resp.text.encode('utf8').decode('utf8'))
            if res['code'] == '0':
                proxy_pool = []
                for item in res['msg']:
                    proxy = 'http://{}:{}'.format(item['ip'], item['port'])
                    proxy_pool.append(proxy)
                return proxy_pool
            else:
                other_logger.error('代理ip获取异常吗，错误代码{}'.format(res['code']))
        return []
    except TimeoutError as e:
        other_logger.error('get proxies failed,look {}'.format(e))
        return []
    # try:
    #     resp = requests.get('http://10.0.12.1:5000/pool/get/https/{}'.format(batch_size))  # 获取通过https校验器的20个ip
    #     if resp.text:
    #         res = json.loads(resp.text.encode('utf8').decode('utf8'))
    #         if res['status_code'] == 200:
    #             proxy_pool = res['pool']
    #             return proxy_pool
    #     return []
    # except TimeoutError as e:
    #     other_logger.error('get proxies failed,look {}'.format(e))
    #     return []


def del_proxy(proxy):
    """
    删除代理ip
    :param proxy:
    :return:
    """
    try:
        resp = requests.get('http://10.0.12.1:5000/proxy/delete?usage=https&proxy={}'.format(proxy))
        if resp.text:
            res = json.loads(resp.text.encode('utf8').decode('utf8'))
            if res['result'] == 'ok':
                return True
        return False
    except TimeoutError as e:
        other_logger.error('del proxy failed,look {}'.format(e))
        return False
