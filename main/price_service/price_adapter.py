#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/7/20 17:24
'''
import requests

if __name__ == '__main__':
    get = requests.get(
        "https://www.zhihu.com/search?type=content&q=%E7%A7%9F%E6%88%BF%E5%B9%B3%E5%8F%B0")
    print(f"【main().get={get.content}】")
