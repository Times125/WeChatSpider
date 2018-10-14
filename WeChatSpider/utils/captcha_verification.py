#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/9/20 19:20
@Description: 
"""
import tempfile
from PIL import Image

__all__ = ["identify_captcha_callback", "identify_captcha_by_human"]


# 验证码识别
def identify_captcha_callback(image):
    # TODO 训练模型实现验证码识别 or 打码平台
    pass


# 人工识别验证码，主要用于测试
def identify_captcha_by_human(image):
    # TODO 训练模型实现验证码识别 or 打码平台
    with open('test.png', 'wb') as f:
        f.write(image)
    with open('test.png','rb') as f:
        img = Image.open(f)
        img.show()
    inpt = input("Input the captcha: ")
    print(inpt)
    return inpt
