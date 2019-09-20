1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 0:55
4  # @File  : conversion_feedback_handler.py
5  # @Author: Ch
6  # @Date  : 2019/7/7
import tornado.web
import tornado
from config import web_config
from util import db_util
from util import web_util
from util import mail_util
import time


class ConversionFeedbackHandler(tornado.web.RequestHandler):

    def post(self):
        post_data = web_util.getPostData(self)
        analysis = post_data.get('analysis_id')
        company = post_data.get('company_id')
        state = post_data.get('state')
        error = post_data.get('error')
        print('feedback from conversion:', analysis, company, state, error)
        # print(type(state))

        if (analysis is None) or (company is None) or (state is None):
            # 基础信息不全
            self.write('some information is missing')
            print('message missing')
            return
        # 检查返回
        if state.lower() == 'true':
            self.write('get your message:true')

            # 获取补充数据
            msg={'analysis_id': analysis, 'company_id': company}
            other_info=web_util.getOtherInfo(msg)
            time_target=other_info.get('time_result')
            other_target=other_info.get('other_result')

            # 调用分析
            msg = {'analysis_id': analysis, 'company_id': company,'time_target':time_target,'other_target':other_target}
            web_util.startService('analysis',msg)
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
                    'SET error= \'2\',error_description=\'%(error)s\' '
                    'WHERE  analysis_id=%(aid)s '
                    'AND  company_id=%(cid)s'
                    % {'error': error, 'aid': analysis, 'cid': company}
                )
                content = (
                        time.strftime("%Y-%m-%d %H:%M", time.localtime()) + '\n' +
                        'analysis id: ' + analysis + '\n' +
                        'company id: ' + company + '\n' +
                        'error message: ' + error + '\n'
                )
                mail_util.sendMail('conversion', 'CriBug feedback:Error of Conversion', content)
                print('error')
            except Exception as err:
                print(err)
