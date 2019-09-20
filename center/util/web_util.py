1  # !/usr/bin/env python
2  # -*- coding: utf-8 -*-
3  # @Time  : 22:16
4  # @File  : web_util.py
5  # @Author: Ch
6  # @Date  : 2019/7/6
import json
import requests
import time
from util import mail_util
from config import web_config
from util import db_util
from tornado import gen


def getPostData(webRes):
    '''
    解析post数据·
    :param webRes:
    :return:
    '''

    post_data = webRes.request.body_arguments
    # print(type(post_data))
    post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}

    if not post_data:
        post_data = webRes.request.body.decode('utf-8')
        post_data = json.loads(post_data)
    return post_data


def getMsg(url, params, headers={}):
    par = '?'
    if params:
        for key in params:
            par += key + '=' + params[key] + '&'
        par = par[:-1]
    else:
        par = ''
    url += par
    print(url)
    res = requests.get(url=url)
    return res


def postMsg(url, msg, headers={}):
    '''
    发送post请求
    :param url:
    :param msg:
    :param headers:
    :return:
    '''
    body = msg
    try:
        print('try to post msg', msg, 'to', url)
        res = requests.post(url=url, data=body, headers=headers)
        # print(res.text)
        return res
    except Exception as err:
        print(err)
        return None


def postStart(targetType, msg, headers={}):
    url = web_config.WebConfig.get(targetType)
    res = postMsg(url, msg)
    analysis = msg.get('analysis_id')
    company = msg.get('company_id')
    if not res is None:
        print('spider success')
    else:
        # 连接出错，更新数据库
        print('fail to start conversion')
        db_util.db_operation.execute_change(
            'UPDATE analysis '
            'SET state = \'-1\',error=\'conversion\''
            'WHERE  analysis_id=%(aid)s '
            'AND  company_id=%(cid)s'
            % {'aid': analysis, 'cid': company}
        )


def startService(targetType, msg):
    url = web_config.WebConfig.get(targetType)
    res = postMsg(url, msg)
    if not res is None:
        print(res.text)
        print('spider success')
    else:
        # 连接出错，更新数据库
        print('fail to start %s' % targetType)
        # 错误登记到数据库 转换未能启动
        db_util.db_operation.execute_change(
            'UPDATE analysis '
            'SET error = \'2\',error_description=\'%(error)s\''
            'WHERE  analysis_id=%(aid)s '
            'AND  company_id=%(cid)s'
            % {'aid': msg.get('analysis_id'), 'cid': msg.get('company_id'), 'error': 'fail to start %s' % targetType}
        )
        content = (
                time.strftime("%Y-%m-%d %H:%M", time.localtime()) + '\n' +
                'analysis id: ' + msg.get('analysis_id') + '\n' +
                'company id: ' + msg.get('company_id') + '\n' +
                'error message: ' + 'fail to start %s' % targetType + '\n'
        )
        mail_util.sendMail('spider', 'CriBug feedback:Error of spider', content)


def getCompanyInfo(company_id):
    res = getMsg(web_config.spider_host + web_config.search_location, {"keyword": company_id})
    return json.loads(res.text)

def getStockInfo(company_id):
    res = getMsg(web_config.spider_host + web_config.message_location, {"company_id": company_id})
    return json.loads(res.text)


def getOtherInfo(msg):
    res = postMsg(web_config.spider_host + web_config.other_location, msg)
    # print(res)
    return json.loads(res.text)


if __name__ == '__main__':
    getOtherInfo('000001')