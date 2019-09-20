1  #!/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 11:34
4  # @File  : request_message_handler.py
5  # @Author: Ch
6  # @Date  : 2019/7/6
import json
import tornado.web
from util import db_util

class UserInfoHandler(tornado.web.RequestHandler):
    def get(self):
        res = db_util.db_operation.execute_query(
            'SELECT user_id,email,'
            'COUNT(if(state=\'0\',true,null)) as countW,'
            'COUNT(if(state=\'1\',true,null))  as countF '
            'FROM user NATURAL JOIN analysis '
            'GROUP BY user_id')
        if not res is None:
            msg=[]
            for record in res:
                msg.append({
                    'userid': record[0],
                    'email': record[1],
                    'workingCount': record[2],
                    'finishedCount': record[3]
                })
            print('get user info')
            res=json.dumps(msg)
            print(res)
            self.write(res)
        else:
            self.write('db fail')


class GeneralMessageHandler(tornado.web.RequestHandler):
    def get(self):
        res = db_util.db_operation.execute_query(
            'SELECT analysis_id,user_id,company_id,created_at,state '
            'FROM analysis '
            'WHERE error=\'0\'')
        if not res is None:
            msg=[]
            for record in res:
                state=record[4]
                if state=='0':
                    state='正在处理'
                elif state=='1':
                    state='处理完成'
                msg.append({
                    'analysis_id':record[0],
                    'user_id':record[1],
                    'company_id':record[2],
                    'created_at':record[3].strftime("%Y-%m-%d %H:%M"),
                    'state':state
                })
            result=json.dumps(msg)
            print('get general message')
            self.write(result)
            # print(type(msg))
        else:
            self.write('db fail')


class ErrorMessageHandler(tornado.web.RequestHandler):

    def get(self):
        res = db_util.db_operation.execute_query(
            'SELECT analysis_id,user_id,company_id,created_at,error,error_description '
            'FROM analysis '
            'WHERE NOT error=\'0\'')
        if not res is None:
            msg=[]
            for record in res:
                msg.append({
                    'analysis_id':record[0],
                    'user_id':record[1],
                    'company_id':record[2],
                    'created_at':record[3].strftime("%Y-%m-%d %H:%M"),
                    'error':record[4],
                    'error_info':record[5]
                })
            result=json.dumps(msg)
            self.write(result)
            # print(type(msg))
        else:
            self.write('db fail')
