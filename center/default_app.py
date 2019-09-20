1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 11:22
4  # @File  : default_app.py
5  # @Author: Ch
6  # @Date  : 2019/7/6
import tornado.ioloop
import tornado.web

from handlers import request_message_handler, \
    crawl_feedback_handler, \
    conversion_feedback_handler, \
    analysis_feedback_handler, \
    add_request_handler, \
    problem_solve_handler,\
    admin_login_handler
from util import db_util
from util import mail_util


def default_app():
    '''
    初始化app
    :return:
    '''
    init()
    return tornado.web.Application([
        (r'/new', add_request_handler.AddRequestHander),

        (r'/feedback/spider', crawl_feedback_handler.CrawlFeedbackHandler),
        (r'/feedback/analysis', analysis_feedback_handler.AnalysisFeedbackHandler),
        (r'/feedback/conversion', conversion_feedback_handler.ConversionFeedbackHandler),

        (r'/user', request_message_handler.UserInfoHandler),
        (r'/normal', request_message_handler.GeneralMessageHandler),
        (r'/error', request_message_handler.ErrorMessageHandler),
        (r'/solve', problem_solve_handler.ProblemSolveHandler),
        (r'/root/login',admin_login_handler.AdminLoginHandler)
    ])
def init():
    db_util.init()
    mail_util.initAdminAddr()
