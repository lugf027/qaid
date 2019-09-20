1  #!/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 16:10
4  # @File  : problem_solve_handler.py
5  # @Author: Ch
6  # @Date  : 2019/7/7
import tornado.web
from util import web_util
from util import db_util


class ProblemSolveHandler(tornado.web.RequestHandler):
    def post(self):
        postdata=web_util.getPostData(self)
        analysis_id=postdata.get('analysis_id')
        company_id=postdata.get('company_id')
        error=postdata.get('error')
        msg = {'analysis_id': analysis_id, 'company_id': company_id}
        if error=='1':
            try:
                db_util.db_operation.execute_change(
                    'UPDATE analysis '
                    'SET error = \'0\',error_description= NULL '
                    'WHERE  analysis_id=%(aid)s'
                    %{'aid':analysis_id})
                print('problem of spider solved')
                self.write('problem of spider solved')
                # 通知转化
                web_util.startService('conversion',msg)
            except Exception as error:
                print(error)
                self.write('db error')
        elif error=='2':
            try:
                db_util.db_operation.execute_change(
                    'UPDATE analysis '
                    'SET error = \'0\',error_description= NULL '
                    'WHERE  analysis_id=%(aid)s'
                    %{'aid':analysis_id}
                )
                print('problem of conversion solved')
                self.write('problem of conversion solved')
                # 通知分析
                web_util.startService('analysis', msg)
            except Exception as error:
                print(error)
                self.write('db error')
        elif error == '3':
            try:
                db_util.db_operation.execute_change(
                    'UPDATE analysis '
                    'SET error = \'0\',error_description= NULL '
                    'WHERE  analysis_id=%(aid)s'
                    % {'aid': analysis_id}
                )
                print('problem of analysis solved')
                self.write('problem of analysis solved')
            except Exception as error:
                print(error)
                self.write('db error')

