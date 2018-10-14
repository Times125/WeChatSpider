#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/8/28 19:53
@Description: common setting for project
"""

# log dir settings
log_dir = "logs_dir"
log_name = "WeChat.log"

# mysql database settings
db_host = '127.0.0.1'
db_port = 3306
db_user = 'root'
db_pwd = ''
db_name = 'WEIXIN'
db_charset = 'utf8mb4'
db_type = 'mysql'

# redis settings
redis_host = '127.0.0.1'
redis_port = 6379
redis_pwd = ''
common_db = 1

# celery settings (redis db number)
broker_db = 2
backend_db = 3

# cookies db
cookies_db = 4
cookies_pool = 'cookies.pool'

# bloom filter settings
bloomfilter_db = 5
bloomfilter_article = "bloomfilter.weixin.article"


# spider settings
adaptive_page = False  # 自动调整爬取最大翻页数，存在多少页就翻多少页(微信搜狗默认只显示100页),会覆盖设定max_search_page和max_search_account_page
max_search_page = 10  # 按关键字搜索文章最大翻页数(微信搜狗只显示100页，警告：此值不要超过100)
max_search_account_page = 10  # 搜索指定公众号最大翻页数
request_retries = 5  # 请求重试最大次数
identify_captcha_retries = 5  # 验证码识别错误最大重试次数
identify_sleep_time = 5  # 验证码重试时间间隔（s）
