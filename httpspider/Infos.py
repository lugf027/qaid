import re
import time
import os

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PyPDF2 import PdfFileReader
import logging


class Infos(object):
    isMatch = False
    timer = 0
    code_dict = {}
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='myapp.log',
                        filemode='w')

    @classmethod
    def addDict(cls, newDict):
        cls.timer += 1
        cls.code_dict['company:%d' % cls.timer] = newDict

    def __init__(self, company_code, site_type="shenjs", wait_time=2, run_timer=0) -> None:
        Infos.timer = len(Infos.code_dict)
        self.company_code = company_code
        self.year = 2018
        self.page_num = 0
        self.pattern = "年度报告$|年度报告（更新后）$"
        self.st_pattern = "^\*ST"
        self.type = site_type
        self.wait_time = wait_time
        self.run_timer = run_timer

    # 爬取入口
    def crawl(self):
        # 设置无头浏览器
        opt = Options()
        opt.headless = True
        browser = webdriver.Chrome(options=opt)
        years = [2014, 2015, 2016, 2017, 2018]
        temp = {}
        for year in years:
            self.year = year
            result = self.crawl_shenjs(browser)
            if result != "fail":
                temp["%d" % year] = os.getcwd() + "\\" + result
        browser.close()
        return temp

    # 爬指定上市公司的数据
    def crawl_shenjs(self, browser):
        # 开始爬取指定公司PDF
        browser.get("http://www.cninfo.com.cn/new/fulltextSearch?keyWord=%s" % "%(code)s %(year)d年年度报告" % {
            'code': self.company_code, 'year': self.year})
        # 设置隐式等待的时间为10
        browser.implicitly_wait(5)
        logging.info("开始匹配,股票代码: %(code)s_%(year)d" % {'code': self.company_code, 'year': self.year})
        clear_fixs = browser.find_elements_by_css_selector("#ul_a_title > tbody > tr")
        if len(clear_fixs) == 0:
            return "fail"
        for clear_fix in clear_fixs:
            title = clear_fix.find_element_by_css_selector(".sub-title").text
            self.isMatch = (re.search(self.pattern, title) is not None)
            if self.isMatch:
                # 得到 pdf 链接
                btn = clear_fix.find_element_by_css_selector(".sub-title a")
                btn.click()
                time.sleep(2)
                # 将browser跳转到第二个选项卡
                browser.switch_to.window(browser.window_handles[1])
                pdf_site = browser.find_element_by_css_selector(
                    "body > div.container.page-filedetail-container > div.page-filedetail.autoFixedHeight > div > div.cols.col-md-8 > div > a.page-filedetail-fullscreen").get_attribute(
                    "href")
                browser.close()
                browser.switch_to.window(browser.window_handles[0])

                # 检测下载超时
                try:
                    logging.info("开始下载,股票代码：%(code)s_%(year)d" % {'code': self.company_code, 'year': self.year})
                    res = requests.get(pdf_site)
                    path = "pdfs\\" + self.company_code + "\\" + self.company_code + "_%d.pdf" % self.year
                    with open(path, "wb") as f:
                        f.write(res.content)
                        f.close()
                    time.sleep(1)
                    # 检测是否损坏
                    PdfFileReader(path)
                    logging.info("下载成功,股票代码: %(code)s_%(year)d" % {'code': self.company_code, 'year': self.year})
                    return path
                except Exception:
                    # 再次爬取、下载
                    logging.warning(
                        "下载失败，重新拉取,股票代码: %(code)s_%(year)d" % {'code': self.company_code, 'year': self.year})
                    print("runtimer%d" % self.run_timer)
                    self.run_timer += 1
                    if self.run_timer >= 3:
                        os.remove(path)
                    return self.crawl_shenjs(browser)
                break
            if self.isMatch:
                break
        return "fail"
