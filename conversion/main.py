import _thread
import os

import requests
from flask import Flask, request
from conversion import conversion_kill_tags
from conversion.conversion_response import TransResponse
from conversion.Upload import Upload

app = Flask(__name__)


@app.route('/')
def index():
    return "hello, vm"


@app.route('/conversion', methods=['POST'])
def conversion():
    company_id = request.form.get("company_id")
    analysis_id = request.form.get("analysis_id")
    try:
        _thread.start_new_thread(pdf2dd, (company_id, analysis_id))
    except:
        print("Error: 无法启动线程")
    return "start converse..."


def pdf2dd(company_id, analysis_id):
    try:
        print("begin: " + str(company_id))
        pdf_path = "../pdfminer.six-master/tools/pdfs/" + company_id
        html_path = "htmls/" + company_id
        if not os.path.isdir(html_path):
            os.mkdir(html_path)

        print("begin pdf2html")
        pdf_files = os.listdir(pdf_path)
        for pdf_file_name in pdf_files:
            print(pdf_file_name)
            complete_pdf_dir = os.path.join(pdf_path, pdf_file_name)
            html_dir_without_dot_html = os.path.join(html_path, pdf_file_name + ".html")
            os.system('python ../pdfminer.six-master/tools/pdf2txt.py -t html ' + complete_pdf_dir +
                      ' > ' + html_dir_without_dot_html)

        print("begin html2ddpro")
        dd_path = "dds/" + company_id
        if not os.path.isdir(dd_path):
            os.mkdir(dd_path)
        html_files = os.listdir(html_path)
        for html_file_name in html_files:
            print(html_file_name)
            complete_html_dir = os.path.join(html_path, html_file_name)
            complete_dd_dir = os.path.join(dd_path, html_file_name + ".ddpro")
            conversion_kill_tags.kill_tags(complete_html_dir, complete_dd_dir)

        # 这里做检查

        trans_response = TransResponse()
        trans_response.company_id = company_id
        trans_response.analysis_id = analysis_id
        trans_response.state = True

        upload = Upload(company_id)
        upload.start_upload()

        requests.post("http://127.0.0.1:8888/feedback/conversion", data=trans_response.getMap())
    except Exception as e:
        trans_response = TransResponse()
        trans_response.company_id = company_id
        trans_response.analysis_id = analysis_id
        trans_response.state = False
        trans_response.error = str(e)
        requests.post("http://127.0.0.1:8888/feedback/conversion", data=trans_response.getMap())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

