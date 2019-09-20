1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 16:17
4  # @File  : mTest_Hello.py
5  # @Author: Ch
6  # @Date  : 2019/7/3
import tornado.ioloop
import tornado.web

from common import db_helper
from config import db_config
from util import web_util


class HelloHandle(tornado.web.RequestHandler):
    def get(self):
        data = int(self.get_query_argument('data'))
        res = data + 10
        self.write(str(res))


class LoginHandle(tornado.web.RequestHandler):
    def prepare(self):
        self.__dbo = db_helper.db_helper_stuff(db_config.DB_STUFF)
        self.__dbo.conn_db()

    def post(self):
        post_data = web_util.getPostData(self)

        usrName = post_data.get('username')
        passwd = post_data.get('password')
        print(usrName, ":", passwd)
        paReal = self.__dbo.execute_query('SELECT Spassword from stuff where SID= %s ' % usrName)
        if paReal:
            if paReal[0][0] == passwd:
                self.write(str(True))
            else:
                self.write(str(False))
        else:
            self.write(str(False))
        # self.write(str(False))


def hello_app():
    return tornado.web.Application([
        (r'/login', LoginHandle),
        (r'/test', HelloHandle),

    ])


if __name__ == '__main__':
    app = hello_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
