1  #!/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 11:19
4  # @File  : main.py
5  # @Author: Ch
6  # @Date  : 2019/7/6
import tornado
import default_app

if __name__ == '__main__':
    app = default_app.default_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
