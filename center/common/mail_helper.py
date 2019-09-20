1  #!/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 10:49
4  # @File  : mail_helper.py
5  # @Author: Ch
6  # @Date  : 2019/7/3
import smtplib
from email.mime.text import MIMEText

d_smtp='smtp.163.com'
d_port=25


def send_mail(username, passwd, recv, title, content, mail_host=d_smtp, port=d_port):
    '''
    邮箱发信工具
    :param username: str 用户名
    :param passwd: str 授权码
    :param recv: str 目标邮箱  用’，‘分隔  ’1@a.cn,2@b.com‘
    :param title:str
    :param content:
    :param mail_host:
    :param port:
    :return:
    '''
    msg = MIMEText(content)
    msg['Subject'] = title
    msg['From'] = username
    msg['To'] = recv
    try:
        smtp=smtplib.SMTP(host=mail_host,port=port)
        smtp.login(username,passwd)
        smtp.sendmail(username,recv.split(','),msg.as_string())
        print("发送成功")
    except smtplib.SMTPException:
        print("发送失败")

if __name__ == '__main__':
    email_user = 'coder_ch@163.com'
    email_pwd = 'cc123456'
    maillist = '2518663435@qq.com'
    title = 'Test'
    content = 'hello, this is a SMTP Test  1'
    send_mail(email_user, email_pwd, maillist, title, content)
