1  #!/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 10:50
4  # @File  : admin_login_handler.py
5  # @Author: Ch
6  # @Date  : 2019/7/8
import tornado.web
import json
from common import db_helper
from config import db_config
from util import db_util
from util import web_util
import datetime


class AdminLoginHandler(tornado.web.RequestHandler):
    def post(self):
        postdata=web_util.getPostData(self)
        username=postdata.get('username')
        password=postdata.get('password')
        print('login',username,password)
        res=db_util.db_operation.execute_query('SELECT password FROM admin WHERE username=\'%s\''%username)
        # print(len(res))
        if not len(res)==0:
            paReal=res[0][0]
            if paReal==password:
                # 登录成功
                self.write('success login')
                print(username,'login success')
            else:
                # 密码错误
                self.write('wrong password')
        else:
            # 用户名错
            self.write('user not exist')
