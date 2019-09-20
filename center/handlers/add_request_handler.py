from abc import ABC

1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 14:47
4  # @File  : add_request_handler.py
5  # @Author: Ch
6  # @Date  : 2019/7/7
import tornado.web
from util import web_util
from config import web_config


class AddRequestHander(tornado.web.RequestHandler, ABC):
    '''
    添加请求转发
    '''

    def post(self):
        postdata = web_util.getPostData(self)
        analysis_id = postdata.get('analysis_id')
        company_id = postdata.get('company_id')
        if analysis_id is None or company_id is None:
            # 信息不全
            self.write('wrong request')
        else:
            # 提交成功
            self.write('get you analysis request %(aid)s of %(cid)s' % {'aid': analysis_id, 'cid': company_id})
            print('new request,start spider')
            res = web_util.postMsg(web_config.spider_host + web_config.spider_location, postdata)
            # print(res.text)
