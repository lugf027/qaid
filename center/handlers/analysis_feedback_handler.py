1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 0:55
4  # @File  : analysis_feedback_handler.py
5  # @Author: Ch
6  # @Date  : 2019/7/7
from tornado import web
from util import mail_util
from util import db_util
from util import web_util
import time



class AnalysisFeedbackHandler(web.RequestHandler):

    def post(self):
        post_data = web_util.getPostData(self)
        analysis = post_data.get('analysis_id')
        company = post_data.get('company_id')
        state = post_data.get('state')
        error = post_data.get('error')
        result=post_data.get('result')
        print('feedback from analysis:', analysis, company, state, error)

        # print(type(state))
        if (analysis is None) or (company is None) or (state is None):
            # 基础信息不全
            self.write('some information is missing')
            print('message missing')
            return
        if state.lower() == 'true':
            self.write('get your message:true')
            # 更新请求状态
            db_util.db_operation.execute_change(
                'UPDATE analysis '
                'SET state = \'0\', error=NULL '
                'WHERE  analysis_id=%(aid)s '
                'AND  company_id=%(cid)s'
                % {'aid': analysis, 'cid': company}
            )
            print('analysis success')

        elif error is None:
            # 报错 error信息缺失
            self.write('error information is missing')
            print('missing error information')
        else:
            # 添加错误信息
            try:
                db_util.db_operation.execute_change(
                    'UPDATE analysis '
                    'SET state = \'-1\',error=\'%(error)s\' '
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
                mail_util.sendMail('analysis', 'CriBug feedback:Error of analysis', content)
                print('error')
            except Exception as err:
                print(err)
            self.write('get your error message')
