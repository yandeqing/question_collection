#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/8/8 9:38
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

bank_namelist=["icbc","ccb","abc","comm","boc","cmbc","psbc","other"]

def open_bank_url(bank_name):
    driver = webdriver.Chrome(
        executable_path=r'./chromedriver.exe',
        options=Options())
    wait = WebDriverWait(driver, 10)
    print("打开银行页面")
    try:
        driver.get(f'http://www.chakahao.com/cardbin/chakahao_{bank_name}.html')
        driver.maximize_window()
        text = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body>center>div:nth-child(4)')))
        str1 = text.text.split(' ')
        print(f"共计{len(str1)}条")
        for i in str1:
            # print(i)
            url = 'http://www.chakahao.com/cardbin/html/{0}.html'.format(i)
            driver.get(url)
            try:
                bank = driver.find_element_by_css_selector(".chalist > p:nth-child(3)")
                bank_number = driver.find_element_by_css_selector(".chalist > p:nth-child(5)")
                if bank:
                    f = open(f"{bank_name}_bank_text.txt", 'a')  # 存储爬取到的银行卡的数据
                    print(bank.text, bank_number.text)
                    print(bank.text, bank_number.text, file=f)
            except:
                print(f"发生异常卡号:{i}",file=f)
                pass

        # driver.quit()
    except TimeoutError:
        print("NO")




if __name__ == '__main__':
    for name in bank_namelist:
        open_bank_url(name)
