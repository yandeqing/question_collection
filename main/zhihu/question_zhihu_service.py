#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/6/26 14:36
'''

import json
import os
import time
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

# 开启委托模式
from main.common import time_util, excel_util

os.system(
    'start chrome.exe --remote-debugging-port=9222 --user-data-dir="F:\selenum\AutomationProfile"')


class ZhiHu:
    def __init__(self):
        time.sleep(3)
        self.title = '知乎 - 有问题，上知乎'
        self.page_source = None
        self.url = 'https://www.zhihu.com/'
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")  # 前面设置的端口号
        self.browser = webdriver.Chrome(
            executable_path=r'./chromedriver.exe',
            options=self.chrome_options)  # executable执行webdriver驱动的文件
        # http://selenium-python.readthedocs.io/waits.html
        # 隐式等待：调用driver.implicitly_wait。那么在获取不可用的元素之前，会先等待10秒中的时间
        self.browser.implicitly_wait(10)
        # self.browser.maximize_window()

    def get_start(self):
        while self.title == '知乎 - 有问题，上知乎':
            self.browser.get(self.url)
            self.title = self.browser.title
            print(self.browser.title)
            # 登陆页面
            if '知乎 - 有问题，上知乎' == self.browser.title:
                span_lable = \
                    self.browser.find_elements_by_xpath(
                        '//div[@class="SignContainer-switch"]/span')[0]
                span_lable.click()
                time.sleep(1.5)
                username = self.browser.find_elements_by_name('username')[0]  # 获取username的input标签
                password = self.browser.find_elements_by_name('password')[0]  # 获取password的input标签
                username.clear()
                password.clear()
                username.send_keys('18711790101')
                password.send_keys('pj409112270')
                time.sleep(1.5)
                button = \
                    self.browser.find_elements_by_xpath(
                        '//button[contains(@class, "SignFlow-submitButton")]')[
                        0]  # 登录按钮
                span_lable = self.browser.find_elements_by_xpath(
                    '//div[contains(@class, SignFlow-captchaContainer)]/div/span[@class="Captcha-englishImage"]')
                if len(span_lable) == 1:  # 判断验证码类型，是中文（点击类型）还是英文（输入类型）的
                    # 英文验证码
                    img_url = span_lable[0].get_attribute('src')  # 验证码图片路径
                    print(f"【login(英文验证码).img_url={img_url}】")
                    if img_url == 'data:image/jpg;base64,null' or img_url == None:  # 判断是否有验证码
                        print('没有验证码,直接点击登录！')
                        button.click()
                    else:
                        print('英文验证码')
                        base64_img_url = img_url.replace('data:image/jpg;base64,', '')  # 对base64做处理
                        print(f"【login().base64_img_url={base64_img_url}】")
                        # make_base64(base64_img_url)
                        input_lable = self.browser.find_elements_by_name('captcha')[0]
                        # show_img()
                        code = input('手动打码，请输入验证码>>>')
                        # code = use_ydm('img_code.png')  # 调用云打码接口，返回识别后的内容
                        input_lable.send_keys(code)  # 将验证码写入
                        button.click()
                    self.save_cookies()
                elif len(span_lable) == 0:
                    # 中文验证码
                    img_lable = \
                        self.browser.find_elements_by_xpath('//img[@class="Captcha-chineseImg"]')[
                            0]  # 查找中文验证码标签
                    if img_lable:
                        img_url = img_lable.get_attribute('src')  # 验证码图片路径
                        print(f"【login(中文验证码).img_url={img_url}】")
                        if img_url == 'data:image/jpg;base64,null' or img_url == None:  # 判断是否有验证码
                            print('没有验证码,直接点击登录！')
                            button.click()
                        else:
                            print('中文验证码')
                    self.save_cookies()
                else:
                    # 没有验证码
                    button.click()
                    self.save_cookies()
        # 首页
        print("已登录!")
        keywords = "租房推荐"
        s = quote(keywords)
        self.save_cookies()
        self.browser.get(f"https://www.zhihu.com/search?type=content&q={s}")
        WebDriverWait(self.browser, 30).until(expected_conditions.title_contains('搜索结果'))
        while self.page_source != self.browser.page_source:
            self.page_source = self.browser.page_source
            print(f"【get_start().self.page_source={len(self.page_source)}】")
            # 滑到底部
            self.browser.execute_script("window.scrollTo(0,1000000)")
            print("滑到底部!")
            time.sleep(3)
        items = self.browser.find_elements_by_xpath('//div[@class="List-item"]')
        print(f"数据加载完毕!总共：{len(items)}条记录")
        pages=[]
        for i, item in enumerate(items):
            title = item.find_element_by_tag_name('a')
            button = item.find_elements_by_xpath('//button[contains(@class,"VoteButton")]')[0]
            # button = item.find_elements_by_xpath('//button[contains(@class,"ContentItem-more")]')[0]
            # if button:
            #     from selenium.webdriver.common.by import By
            #     WebDriverWait(self.browser, 10).until(expected_conditions
            #                                           .element_to_be_clickable(
            #         (By.XPATH, '//button[contains(@class,"VoteButton")]')))
            #     webdriver.ActionChains(self.browser).move_to_element(button).click(button).perform()
            #     time.sleep(15)
            texts = item.text.split('\n')
            href = title.get_attribute("href")
            if len(texts) > 1:
                print(f"{i}.\n问：{texts[0]}\n答：{texts[1]}\nhref:{href}")
                pages.append({'question':texts[0],'answer':texts[1],'href':href})
        date = time_util.now_to_date('%Y%m%d_%H%M')
        filename = date + keywords + "_zhihu.xls"
        excel_util.write_excel(filename=filename, worksheet_name=date, items=pages)
        print(f"【main().html=总共有{len(pages)}条数据】")
        for item in pages:
            import requests
            post = requests.post(url="http://localhost:8080", json=item)
            print(f"【main().post={post}】")

    def save_cookies(self):
        # 检验是否登陆！
        try:
            WebDriverWait(self.browser, 3).until(expected_conditions.title_contains('首页'))
        except Exception as e:
            print(f"Exception:{e}")
            time.sleep(3)
            return
        # time.sleep(20)  # 可以选择手动登录或者是自动化，我这里登录过就直接登陆了
        info = self.browser.get_cookies()  # 获取cookies
        print(info)
        with open(r".\info.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(info))
        self.title = self.browser.title


if __name__ == '__main__':
    zhihu = ZhiHu()
    zhihu.get_start()
