1  #!/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 20:18
4  # @File  : t_web.py
5  # @Author: Ch
6  # @Date  : 2019/7/6
import requests
from util import web_util
from config import web_config
import json

def t_post():
    url = 'http://localhost:8888/feedback/spider'
    body = {'analysis_id': 6, 'company_id': '000002', 'state': 'true'}
    headers = {}
    res = requests.post(url=url, data=body, headers=headers)
    print(res.text)


def t_crawl():
    res=web_util.getMsg(web_config.spider_host+web_config.search_location, {"keyword":'000001'})
    print(res.text)


if __name__ == '__main__':
    # t_post()
    t_crawl()