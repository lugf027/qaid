1  #!/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 9:37
4  # @File  : mail_util.py
5  # @Author: Ch
6  # @Date  : 2019/7/9
from common import mail_helper
from config import mail_config
from util import db_util
from config import mail_config


def sendMail(receiver,title,content):
    recvs=mail_config.mail_addrs_admin.get(receiver)
    recv=''
    for str in recvs:
        recvs=str+','
    recv=recvs[:-1]
    # print(recv)
    mail_helper.send_mail(
        username=mail_config.admin.get('user'),
        passwd=mail_config.admin.get('passwd'),
        recv=recv,
        title=title,
        content=content,
        mail_host=mail_config.default_host.get('host'),
        port=mail_config.default_host.get('port')
    )


def initAdminAddr():
    res=db_util.db_operation.execute_query(
        "SELECT  access,email FROM admin"
    )
    for tuple in res:
        if  tuple[0] == '1':
            mail_config.mail_addrs_admin.get('spider').append(tuple[1])
        elif tuple[0] == '2':
            mail_config.mail_addrs_admin.get('conversion').append(tuple[1])
        elif tuple[0] == '3':
            mail_config.mail_addrs_admin.get("analysis").append(tuple[1])
    # print(mail_config.mail_addrs_admin)


