import sys
import time

import requests
import xlwt
from lxml import etree
from selenium import webdriver


class ContentFocus:
    def __init__(self):
        self.search_data = sys.argv[1]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
        }
        self.url = "https://www.alibaba.com"

        self.urls_list = []

    def request_url_to_save_excel(self, url_list):
        # 创建一个excel
        excel = xlwt.Workbook()
        # 添加工作区
        sheet = excel.add_sheet("数据")

        # 标题信息
        head = ["标题", "关键词"]
        for index, value in enumerate(head):
            sheet.write(0, index, value)

        for index, detail_url in enumerate(url_list, 1):
            data = requests.get("https:" + detail_url, headers=self.headers)
            detail = etree.HTML(data.text)
            detail_data = detail.xpath('/html/head/meta[@name="keywords"]/@content')
            value_list = detail_data[0].split("- Buy")
            for i, value in enumerate(value_list):
                sheet.write(index, i, value)

        # 保存excel
        excel.save("./write.xls")

    def start(self):
        driver = webdriver.Chrome(executable_path="./webdriver/chromedriver.exe")
        driver.get(self.url)
        search = driver.find_element_by_class_name("ui-searchbar-keyword")
        print(self.search_data)
        search.send_keys(self.search_data)
        button = driver.find_element_by_xpath('//*[@id="J_SC_header"]/header/div[2]/div[3]/div/div/form/input[4]')
        driver.execute_script("arguments[0].click();", button)
        while True:
            time.sleep(5)
            pagination = driver.find_element_by_xpath(
                '//*[@id="root"]/div//div//a[@class="seb-pagination__pages-link pages-next"]')
            driver.execute_script("arguments[0].scrollIntoView();", pagination)
            html = etree.HTML(driver.page_source)
            parse_html = html.xpath(
                '//*[@id="root"]//div[@class="offer-list-wrapper"]//div[@data-content="abox-ProductNormalList"]//div/a[@class="organic-gallery-offer__img-section"]/@href')
            for detail_url in parse_html:
                if len(self.urls_list) < 100:
                    self.urls_list.append(detail_url)

            if len(self.urls_list) < 100:
                driver.execute_script("arguments[0].click();", pagination)
                continue
            else:
                break
        driver.close()
        self.request_url_to_save_excel(self.urls_list)


if __name__ == '__main__':
    content = ContentFocus()
    content.start()
