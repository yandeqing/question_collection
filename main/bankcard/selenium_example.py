#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/8/8 9:38
'''
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def open_bank_url():
    os.system(
        'start chrome.exe --remote-debugging-port=9222 --user-data-dir="F:\selenum\AutomationProfile"')
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 前面设置的端口号
    driver = webdriver.Chrome(
        executable_path=r'./chromedriver.exe',
        options=options)
    # driver.implicitly_wait(2)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get('https://www.jlshare.top/bankCard')
        # driver.maximize_window()
        wait.until(
            EC.presence_of_element_located((By.ID, 'banck')))
        trs = driver.find_elements_by_xpath("//table[@id='banck']/tbody/tr")
        bankcard={}
        for i in trs:
            i.click()
            print(i.text)
            subtrs = i.find_elements_by_xpath("//table[@id='subbanck']/tbody/tr")
            for sub in subtrs:
                sub.click()
                print(sub.text)
                cardNoList = i.find_elements_by_xpath("//table[@id='cardNoList']/tr")
                for card in cardNoList:
                    f = open("banknumbers.txt", 'a')  # 存储爬取到的银行卡的数据
                    print(sub.text, card.text, file=f)
                    print(sub.text, card.text)

        # driver.quit()
    except Exception  as e:
        print(f"{e}")


if __name__ == '__main__':
    open_bank_url()
