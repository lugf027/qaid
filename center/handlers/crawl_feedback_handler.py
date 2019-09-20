1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 19:06
4  # @File  : crawl_feedback_handler.py
5  # @Author: Ch
6  # @Date  : 2019/7/6
import tornado.gen
import tornado.web

from config import web_config
from util import db_util
from util import web_util
from util import mail_util
import time
import json


class CrawlFeedbackHandler(tornado.web.RequestHandler):

    def post(self):
        post_data = web_util.getPostData(self)
        analysis_id = post_data.get('analysis_id')
        company_id = post_data.get('company_id')
        state = post_data.get('state')
        error = post_data.get('error')
        print('feedback from spider:', analysis_id, company_id, state, error)
        # print(type(state))

        if (analysis_id is None) or (company_id is None) or (state is None):
            # 基础信息不全
            self.write('some information is missing')
            print('message missing')
            return
        # 检查返回
        if state.lower() == 'true':
            self.write('get your message:true')

            # 调用文件转换
            msg = {'analysis_id': analysis_id, 'company_id': company_id}
            web_util.startService('conversion', msg)

            # 获取公司实时信息并上传到数据库
            company_info = web_util.getCompanyInfo(company_id)
            if (company_info.get('status') == 'success'):
                company_info.pop('status')
                # 将四个值保存到数据库
                db_util.db_operation.execute_change(
                    'UPDATE analysis '
                    'SET company_digit=\'%(company_digit)s\' '
                    'WHERE  analysis_id=%(aid)s '
                    'AND  company_id=%(cid)s'
                    % {'company_digit': company_info, 'aid': analysis_id, 'cid': company_id}
                )
            else:
                db_util.db_operation.execute_change(
                    'UPDATE analysis '
                    'SET  error= \'1\',error_description=\'%(error)s\' '
                    'WHERE  analysis_id=%(aid)s '
                    'AND  company_id=%(cid)s'
                    % {'error': 'fail to get company digit', 'aid': analysis_id, 'cid': company_id}
                )

            # 获取股票信息
            company_stock = web_util.getStockInfo(company_id)
            db_util.db_operation.execute_change(
                'UPDATE analysis '
                'SET company_stock=\'%(company_stock)s\' '
                'WHERE  analysis_id=%(aid)s '
                'AND  company_id=%(cid)s'
                % {'company_stock': company_stock, 'aid': analysis_id, 'cid': company_id}
            )

        # 返回：出错
        else:
            if error is None:
                # 报错 error信息缺失
                error = 'unknown error from spider'
                self.write('error information is missing')
                print('missing error')
            else:
                self.write('get your error message')

            try:
                # 将返回的错误信息登记到数据库
                db_util.db_operation.execute_change(
                    'UPDATE analysis '
                    'SET error= \'1\',error_description=\'%(error)s\' '
                    'WHERE  analysis_id=%(aid)s '
                    'AND  company_id=%(cid)s'
                    % {'error': error, 'aid': analysis_id, 'cid': company_id}
                )
                content = (
                        time.strftime("%Y-%m-%d %H:%M", time.localtime()) + '\n' +
                        'analysis id: ' + analysis_id + '\n' +
                        'company id: ' + company_id + '\n' +
                        'error message: ' + error + '\n'
                )
                mail_util.sendMail('spider', 'CriBug feedback:Error of spider', content)
                print('spider error:', error)
            except Exception as err:
                print(err)
