1  #!/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 15:54
4  # @File  : db_util.py
5  # @Author: Ch
6  # @Date  : 2019/7/6
from common import  db_helper
from config import db_config


db_operation=db_helper.DBHelper
def init():
    '''
    根据db_admin初始化数据库工具
    :return:
    '''
    global db_operation
    db_operation = db_helper.init_db(db_config.DB_Admin)