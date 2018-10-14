## WeChatSpider
[![](https://img.shields.io/badge/python-3-brightgreen.svg)](https://www.python.org/downloads/)
[![](https://img.shields.io/pypi/l/Django.svg)](LICENSE)

## 项目简介
基于celery和requests的分布式微信爬虫,目前需要做的是突破cookies,分析js；

## 如何使用
1. 按照配置文档配置系统所需环境
2. release页面下载稳定版程序
3. 安装程序所需依赖
4. 创建数据库表单 `python initialize.py`
5. 运行`celery -A WeChatSpider.tasks.workers worker` 启动worker
6. 
## 注意事项
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


