1  #!/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 10:48
4  # @File  : db_helper.py
5  # @Author: Ch
6  # @Date  : 2019/7/3
import pymysql

class DBHelper():
    __host='localhost'
    __port=3306


    def __init__(self,db_info):
        self.connect = None
        self.cursor = None
        # 初始化数据库参数
        # 数据库名称
        self.db_name = db_info['db_name']
        # 用户名
        self.db_user = db_info['db_user']
        # 密码
        self.db_pass = db_info['db_pass']
        # 服务器
        self.db_host = db_info['db_host']
        # 端口
        self.db_port = db_info['db_port']

    # 建立连接  创建游标
    def conn_db(self):
        print('Start try to conn')
        try:
            self.connect=pymysql.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_pass,
                database=self.db_name,
                charset='utf8'
            )
            self.cursor=self.connect.cursor()
            print('connect to db',self.db_name,'successfully')
            return True
        except Exception as err:
            print(err)
            return False

    #关闭数据库
    def close_db(self):
        try:
            self.cursor.close()
            self.connect.close()
            return True
        except pymysql.err as err:
            print(err)
            return False

    def execute_query(self,query):
        '''
        :param query:SQL语句
        :param res_type: 匹配类型（'one'/'all'/1234(匹配数)）
        :return: 结果/none
        '''
        if not query:
            return None
        else:
            try:
                self.cursor.execute(query)
                print("query successfully")
                return self.cursor.fetchall()
            except Exception as err:
                print('query fail',err)
    def execute_change(self,query):
        '''
                :param query:SQL语句
                :param res_type: 匹配类型（'one'/'all'/1234(匹配数)）
                :return: 结果/none
                '''
        if not query:
            return None
        else:
            try:
                self.cursor.execute(query)
                self.connect.commit()
                print("db commit successfully")
                return self.cursor.fetchall()
            except Exception as err:
                print('query fail', err)
def init_db(db_info):
    res=DBHelper(db_info=db_info)
    if res.conn_db():
        return res
    else:
        return None
