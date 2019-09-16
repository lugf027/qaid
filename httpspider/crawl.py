from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import  time
import json

def crawl(keyword):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://www.iwencai.com/stockpick/search?w="+keyword)
    wait = WebDriverWait(driver, 10)
    try:
        #总市值
        tot_property=wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='dp_tablemore_3']/div/div/div/div/table/tbody/tr/td[1]/div/a"))).text
        #市盈率
        Pe_ratio=wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='dp_tablemore_3']/div/div/div/div/table/tbody/tr/td[5]/div/a"))).text
        driver.get("http://www.iwencai.com/stockpick/search?w=" + keyword+ "经营现金流")
        #经营现金流
        cash_flow = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#dp_block_0 > div > table > tbody > tr:nth-child(2) > td > div > a")
            )).text
        driver.get("http://www.iwencai.com/stockpick/search?w=" + keyword + "净利润增长率")
        #净利润增长率
        profit_growth_rate = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='dp_block_0']/div/table/tbody/tr[2]/td/div/a")
            )).text
        dict={
            "status": "success",
            "tot_property": tot_property,
            "Pe_ratio": Pe_ratio,
            "cash_flow": cash_flow,
            "profit_growth_rate":profit_growth_rate
        }
        driver.close()
        return json.dumps(dict)
    except Exception as reason:
        print(reason)
        return json.dumps({"status":"fail"})


if __name__ == "__main__" :
    crawl("000001")
