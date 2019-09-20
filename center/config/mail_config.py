1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 9:25
4  # @File  : mail_config.py
5  # @Author: Ch
6  # @Date  : 2019/7/9
from util import db_util

mail_163 = {'host': 'smtp.163.com', 'port': 25}
mail_126 = {'host': 'smtp.126.com', 'port': 25}
mail_netease = {'host': 'smtp.netease.com', 'port': 25}
mail_qq = {'host': 'smtp.qq.com', 'port': 465}
mail_qq_ = {'host': 'smtp.qq.com', 'port': 587}

admin = {'user': 'coder_ch@163.com', 'passwd': 'cc123456'}
default_host = mail_163
mail_addrs_admin = {'spider': [], 'conversion': [], 'analysis': []}
