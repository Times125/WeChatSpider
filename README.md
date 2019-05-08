## WeChatSpider
[![](https://img.shields.io/badge/python-3-brightgreen.svg)](https://www.python.org/downloads/)
[![](https://img.shields.io/pypi/l/Django.svg)](LICENSE)
[![](https://img.shields.io/badge/WeChatSpider-tets-yellowgreen.svg)](https://github.com/Times125/WeChatSpider)
[![](https://img.shields.io/badge/celery-4-brightgreen.svg)](http://www.celeryproject.org/)

## 项目简介
基于celery和requests的分布式微信爬虫

## 如何使用
1. 按照配置文档配置系统所需环境
2. release页面下载稳定版程序
3. 安装程序所需依赖
4. 创建数据库表单 `python initialize.py`
5. 运行`celery -A WeChatSpider.tasks.workers worker` 启动worker
6. 

## 注意事项

### 看前告知：这还是一个未完成的项目，大家有兴趣可以点个星星，功能会陆续完善

 - 如果遇到运行过程中插入数据库报error:1366，请检查你的数据库字符编码集是否为UTF-8，通过使用以下SQL查看：
```SQL
show variables like '%char%';
```

如果非`utf-8`，通过使用以下SQL更改数据库字符编码集：
```SQL
set character_set_database = utf8mb4;
set character_set_server = utf8mb4;
set character_set_client = utf8mb4;
set character_set_connection = utf8mb4;
set character_set_results = utf8mb4;
```

- 微信搜狗反爬虫机制重点在cookies上，目前经过测试来说，cookies只需要构造两个字段：一个是SUV，另外一个是SNUID。
SUV这个字段可以随机构造一组值，然后md5就行了；SNUID这个值我没找到客户端是怎么生成的，应该是服务器生成的值。
本爬虫想要能够抓到数据，cookies池是非常重要的，我测试的时候使用的是使用浏览器，拿到cookies值，然后cookies池中。
如果是非登录的cookies，只能翻10页。如果是账号登录的cookies可以翻100页。

- 过验证码：有两个方案。方案一是接入三方打码平台；方案二是自己训练模型；


