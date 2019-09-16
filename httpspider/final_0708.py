import _thread
import json
import os

import requests
from flask import Flask, request
from Infos import Infos
from SpiderResponse import Response
from Upload import Upload
from crawl import crawl
from spider_stock import Stock
from analysis_other_targets import OtherTargets

app = Flask(__name__)


@app.route('/spider', methods=['POST'])
def start_to_spider():
    # 获取股票代码参数
    company_id = request.form.get("company_id")
    analysis_id = request.form.get("analysis_id")

    html_path = "pdfs/" + company_id
    os.mkdir(html_path)
    print(html_path)
    print(html_path)
    try:
        _thread.start_new_thread(getPdf, (company_id, analysis_id))
    except:
        return "Error: 无法启动线程"
    return "start crawl..."


def getPdf(company_id, analysis_id):
    # 调用爬取函数
    myInfo = Infos(company_id)

    paths = myInfo.crawl()
    print(paths)
    # 自定义返回体
    response = Response()
    if len(paths) >= 0:
        response.company_id = company_id
        response.analysis_id = analysis_id
        response.state = True
        print(paths)

        # 上传pdf至服务器
        upload = Upload(company_id)
        upload.start_upload()

        requests.post("http://47.93.40.32:8888/feedback/spider", data=response.getMap())
    else:
        response.company_id = company_id
        response.analysis_id = analysis_id
        response.state = False
        response.error = "请求超时"
        requests.post("http://47.93.40.32:8888/feedback/spider", data=response.getMap())


@app.route("/search", methods=['GET'])
def server():
    condition = request.args.get('keyword')
    return crawl(condition)


@app.route("/analysis_other_targets", methods=['POST'])
def analysis_other_targets():
    company_id = request.form.get("company_id")
    other_target = OtherTargets(company_id=company_id)
    return other_target.get_targets()

@app.route("/stock", methods=['GET'])
def crawl_stock():
    id = request.args.get('company_id')
    stock = Stock(id)
    return stock.get_data()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
