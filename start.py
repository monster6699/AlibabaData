import time

import requests
from lxml import etree
from selenium import webdriver

def start():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
    }
    # data = requests.get(url="https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=jacket", headers=headers)
    url = "https://www.alibaba.com"
    driver = webdriver.Chrome(executable_path="./webdriver/chromedriver.exe")
    driver.get(url)
    search = driver.find_element_by_class_name("ui-searchbar-keyword")
    search.send_keys("apple")
    button = driver.find_element_by_xpath('//*[@id="J_SC_header"]/header/div[2]/div[3]/div/div/form/input[4]')
    driver.execute_script("arguments[0].click();", button)

    # 将滚动条移动到页面的底部
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    time.sleep(3)


    html = etree.HTML(driver.page_source)


    # parse_html = html.xpath('//*[@id="root"]//div[@class="offer-list-wrapper"]//div[@class="list-no-v2-left"]/a/@href')
    parse_html = html.xpath('//*[@id="root"]//div[@class="offer-list-wrapper"]//div[@data-content="abox-ProductNormalList"]//div/a[@class="organic-gallery-offer__img-section"]/@href')
    print(len(parse_html))
    for detail_url in parse_html:
        data = requests.get("https:" + detail_url, headers=headers)
        detail = etree.HTML(data.text)
        detail_data = detail.xpath('/html/head/meta[@name="keywords"]/@content')
        print(detail_data)


if __name__ == '__main__':
    start()