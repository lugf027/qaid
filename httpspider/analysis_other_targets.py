import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json


# HOW TO USE：
# instance_name = OtherTargets(company_id = XXXXXX)
# time_target, other_target = instance_name.get_targets()
class OtherTargets(object):
    def __init__(self, company_id=None, years=None, browser=None):
        opt = Options()
        opt.headless = True
        self.isOutBrowser = False
        if browser is None:
            self.browser = webdriver.Chrome(options=opt)
        else:
            self.isOutBrowser = True
        if years is None:
            years = ["2018", "2017", "2016", "2015", "2014"]
        self.company_id = company_id
        self.years = years

    def get_targets(self):
        # 格式 [2018, 2017, 2016, 2015, 2014]
        # 每个年元素：第一季度， 半年报二个月， 半年报一个月， 第三季度， 年报四个月， 年报二个月
        # 其中 0:超期未发布， 1：按时发布， 2:无
        time_result = []
        for year in self.years:
            time_result.append(self.get_time_by_year(year))
        if not self.isOutBrowser:
            self.browser.close()

        # 格式 [超时为0， 不真实为0， 非标准无保留意见为0]
        other_result = []
        out_time = ["600518", "300028", "600656", "400067", "002306", "601558", "600598", ]
        if str(self.company_id) in out_time:
            other_result.append(0)
        else:
            other_result.append(1)

        not_true = ["600610", "600145", "000693", "002680", "002263", "000007", ]
        if str(self.company_id) in not_true:
            other_result.append(0)
        else:
            other_result.append(1)

        do_not_know_describe = ["002362", "002124", "300156", "000930", "002362",
                                "000657", "002471", "000930", "300029", "300029",
                                "300029", "300277", "300033", "002122", "002613",
                                "002289", "300142", "000915", "000520", "000536",
                                "002012", "300277", "300033", "300086", "300086",
                                "300317", "002122", "002509", "300156", "002496",
                                "000417", "002289", "300033", "300169", "300033",
                                "000417", "002289", "000611", "000982", "000982",
                                "002289", ]
        if str(self.company_id) in do_not_know_describe:
            other_result.append(0)
        else:
            other_result.append(1)

        # return time_result, other_result
        return json.dumps({"time_result":time_result, "other_result":other_result})
        
    def get_time_by_year(self, year):
        result = []
        time = self.get_time_from_cninfo(year, "第一季度报告")
        if time == "No report":
            result.append(2)
        elif time.split('-')[1] == "04":
            result.append(1)
        else:
            result.append(0)

        time = self.get_time_from_cninfo(year, "半年度报告")
        if time == "No report":
            result.append(2)
            result.append(2)
        elif time.split('-')[1] == "07":
            result.append(1)
            result.append(1)
        elif time.split('-')[1] == "08":
            result.append(1)
            result.append(0)
        else:
            result.append(0)
            result.append(0)

        time = self.get_time_from_cninfo(year, "第三季度报告")
        if time == "No report":
            result.append(2)
        elif time.split('-')[1] == "10":
            result.append(1)
        else:
            result.append(0)

        time = self.get_time_from_cninfo(year, "年度报告")
        if time == "No report":
            result.append(2)
            result.append(2)
        elif time.split('-')[1] == "01" or time.split('-')[1] == "02":
            result.append(1)
            result.append(1)
        elif time.split('-')[1] == "03" or time.split('-')[1] == "04":
            result.append(1)
            result.append(0)
        else:
            result.append(0)
            result.append(0)
        return result

    def get_time_from_cninfo(self, year, param):
        time = "No report"
        self.browser.get(
            "http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=%(code)s %(year)s年%(param)s" % {
                "code": self.company_id, "year": year,
                "param": param})
        # 设置隐式等待的时间为10
        self.browser.implicitly_wait(2)
        clear_fixs = self.browser.find_elements_by_css_selector(
            "#ul_a_title > tbody > tr")
        if len(clear_fixs) == 0:
            return time
        for clearFix in clear_fixs:
            sleep(0.5)
            title = clearFix.find_element_by_css_selector(".sub-title").text
            is_match = (
                    re.search("(报告|报告正文|报告全文|报告（更新后）|报告全文（更新后）|报告正文（更新后）|报告（全文）|报告（正文）)$", title) is not None)
            if is_match:
                time = clearFix.find_element_by_css_selector(".sub-time").text
                return time
        return time
