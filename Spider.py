#!/usr/bin/python3

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from logger import logger

"""
爬取网络图片
"""


class Spider:
    def __init__(self, url):
        self.url = url

    # 执行脚本
    def runSpider(self):
        driver = webdriver.Chrome()
        # 窗口最大化
        driver.maximize_window()
        # 打开窗口
        driver.get(self.url)
        # 获取图片
        self.getImageList(driver)

    # 获取图片信息
    def getImageList(self, driver):
        try:
            # 执行js脚本
            for i in range(1, 9):
                js = "document.documentElement.scrollTop = document.documentElement.scrollHeight * {} / 10".format(i + 1)
                driver.execute_script(js)
            logger.info(driver.current_url)
            # 获取结果集
            elems = driver.find_elements(By.CSS_SELECTOR, '.segment .tagbqppdiv')
            for ele in elems:
                direction = {
                    'href': ele.find_element(By.CSS_SELECTOR, '.image').get_attribute('src'),
                    'name': ele.find_element(By.CSS_SELECTOR, '.image').get_attribute('alt')
                }
                # 此处可以操作数据库，将数据进行入口操作
                logger.info(direction)
            time.sleep(5)
            # 页码切换
            self.changePage(driver)
        except Exception as e:
            logger.info('获取图片信息失败：{}'.format(e))

    # 页码转换
    def changePage(self, driver):
        # 获取节点
        try:
            pages = driver.find_elements(By.CSS_SELECTOR, '.pagination a')
            for page in pages:
                if page.text == '下一页':
                    page.click()
                    time.sleep(2)
                    self.getImageList(driver)
        except Exception as e:
            logger.info('获取页码节点页失败：{}'.format(e))


if __name__ == '__main__':
    Spider = Spider('https://fabiaoqing.com/biaoqing')
    Spider.runSpider()
