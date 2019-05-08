#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/20 19:20
@Description: 
"""
import io
import base64
import requests
from ..decorators import timeout_decorator
from PIL import Image
from ..config import (captcha_host, captcha_port)

__all__ = ["identify_captcha"]

_captcha_platform_url = 'http://{}:{}/captcha/v1'.format(captcha_host, captcha_port)


@timeout_decorator
def identify_captcha(img_bytes, model_type='sogou', site='sogou.com'):
    """
    通用识别搜狗和腾讯的验证码（6位与4位）
    :param img_bytes: 图片二进制流
    :param model_type: 模型类型，用于标识使用哪个模型来识别此验证码
    :param site: 打码网站，用于标识使用哪个模型来识别此验证码，优先级site > type
    :return:
    """
    # data_stream = io.BytesIO(img_bytes)
    # pil_image = Image.open(data_stream)
    # pil_image.show()
    api_params = {
        'image': base64.b64encode(img_bytes).decode(),
        'model_type': model_type,
        'model_site': site,
    }
    resp = requests.post(_captcha_platform_url, json=api_params).json()
    if resp.get('success') is True:
        code = resp.get('message')
    else:
        code = ''
    return code


def identify_tencent_captcha_callback(img_bytes):
    """
    识别腾讯平台验证码（4位）
    :param img_bytes: 图片二进制流
    :return:
    """
    # TODO 训练模型实现验证码识别
    api_params = {
        'image': base64.b64encode(img_bytes).decode(),
    }

    return 'EFBC'
