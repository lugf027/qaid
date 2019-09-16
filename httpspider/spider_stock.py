from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import json


class Stock:
    # 爬取股票的年份
    years = ["2018", "2017", "2016", "2015", "2014"]

    # 公司代码
    company_code = ""

    # 网址
    url = "http://quotes.money.163.com/trade/lsjysj_%(code)s.html?year=%(year)s&season=4"

    selector_str = "body > div.area > div.inner_box > table > tbody > tr:nth-child(1)"

    # 浏览器
    browser = None

    

    def __init__(self, code):
        self.year_price = []
        self.company_code = code
        op = Options()
        op.headless = True
        self.browser = webdriver.Chrome(options=op)

    def crawl_each_stock(self):
        # 完善网址
        for each_year in self.years:
            true_url = self.url % {"code": self.company_code, "year": each_year}

            # 打开网页
            self.browser.get(true_url)

            # 获取顶行数据
            try:
                WebDriverWait(self.browser, 5).until(lambda e: e.find_element_by_css_selector(self.selector_str))
                top_row = self.browser.find_element_by_css_selector(self.selector_str)
            except Exception:
                break

            # 获取第五列数据
            price = top_row.find_element_by_css_selector("td:nth-child(5)").text

            # 将查询结果加入数组
            self.year_price.append({"year": each_year, "price": price})

    def get_data(self):
        self.crawl_each_stock()
        self.browser.close()
        return json.dumps(self.year_price)
