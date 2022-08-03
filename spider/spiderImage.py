#!/usr/bin/python3

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from db import models
from db.crud import image


class spiderImage:
    def __init__(self, url):
        self.driver = webdriver.Chrome("C://Users/v_llongfang/Desktop/Sign/chromedriver.exe")
        self.url = url

    def get_url(self):
        """
        todo:执行脚本
        :return:
        """
        self.driver.maximize_window()
        self.driver.get(self.url)
        time.sleep(2)
        self.save_image()

    def page_change(self):
        """
        todo:页面切换
        :return:
        """
        for item in self.driver.find_elements(By.CSS_SELECTOR, '.pagination li .page-link'):
            if item.text == '›':
                item.click()
        self.save_image()

    def save_image(self):
        """
        todo:保存图片
        :return:
        """
        print(self.driver.current_url)
        for i in range(0, 9, 2):
            time.sleep(1)
            js = "document.documentElement.scrollTop = document.documentElement.scrollHeight * {} / 10".format(i)
            self.driver.execute_script(js)
        time.sleep(1)
        # 获取图片内容
        try:
            images = self.driver.find_elements(By.CSS_SELECTOR, '.page-content a')
            for item in images:
                url = item.find_element(By.CSS_SELECTOR, '.img-responsive').get_attribute('data-original')
                name = item.find_element(By.CSS_SELECTOR, '.img-responsive').get_attribute('alt')[:50]
                if name is None:
                    name = '斗图啦~'
                if image.get([models.Image.href == url]):
                    print('current url exists: {}'.format(url))
                else:
                    image.save(models.Image(href=url, name=name, width='0', height='0'))
                    print('current url save successfully: {}'.format(url))
        except Exception as e:
            print('error message: {}'.format(e))
        self.page_change()


if __name__ == "__main__":
    spider = spiderImage('https://www.pkdoutu.com/photo/list/')
    spider.get_url()
