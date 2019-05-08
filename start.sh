#! /bin/bash
echo "启动微信爬虫... ..."
source activate lch_spider
nohup python execute_wechat_article.py &
nohup python execute_wechat_monitor.py &
echo '启动完成!'

