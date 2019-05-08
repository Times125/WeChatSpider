#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author:_defined
@Time:  2018/8/28 19:53
@Description: common setting for project
"""

# kafka settings
kafka_server = ['127.0.0.1:9092',]
kafka_topics = ['kafka-topic', ]

# log dir settings
log_dir = "logs_dir"
log_name = "WeChat.log"

# mysql database settings
db_host = '127.0.0.1'
db_port = 3306
db_user = 'root'
db_pwd = 'password'
db_name = 'wechat'
db_charset = 'utf8mb4'
db_type = 'mysql'

# redis settings
redis_host = '127.0.0.1'
redis_port = 6379
redis_pwd = ''
common_db = 1

# cookies db
cookies_db = 1
cookies_pool = 'cookies.pool'

# bloom filter settings
bloomfilter_db = 1
bloomfilter_wexin_sogou = "weixin_sogou.bloomfilter"

# spider settings
max_search_page = 10  # 未登陆只可查看10页，登陆最多只可查看100页
request_retries = 5  # 请求重试最大次数
'''
gzh_crawl_mode 公众号采集模式，可选参数['strict','greed']
'strict'表示只抓取与输入关键字严格匹配的公众号，'greed'表示抓取所有检索到的公众号
'''
gzh_crawl_mode = 'strict'

# spider update time (second)
update_internal = 2 * 60 * 60

# captcha platform settings
captcha_host = '127.0.0.1'
captcha_port = 5000
identify_captcha_retries = 5  # 验证码识别错误最大重试次数
identify_sleep_time = 2  # 验证码重试时间间隔（s）
