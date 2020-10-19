#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/8/17 16:56
'''
import json
import os
import random
import re

import requests

from main.bankcard import BankNumGenerator, BankSimplefy
from main.common import FilePathUtil, excel_util, unionpay_util
from main.common.LogUtil import LogUtil


def getBankInfo(num_generator):
    try:
        # url = f'http://192.168.5.119:5000/bankcard?card_id={num_generator}'
        url = f'http://elklog.zuker.im/bankcard?card_id={num_generator}'
        print(url)
        result = requests.get(url)
        jsons = result.json()
        dumps = json.dumps(jsons, ensure_ascii=False, indent=4)
        print(f'{dumps}')
        return jsons
    except Exception as e:
        print(f"{e}")

def get_chakahao(num_generator):
    try:
        url = f'http://m.chakahao.com/CKHcard'
        print(url)
        data={}
        data['card']=num_generator
        result = requests.post(url=url,data=data)
        text = result.text
        print(f'{text}')
        return text
    except Exception as e:
        print(f"{e}")


if __name__ == '__main__':
    # getBankInfo('')
    # getBankInfo('~')
    # getBankInfo('1212')
    # getBankInfo('1212 1212')
    # getBankInfo('121212222222222222121212')
    # getBankInfo('6213820207881644316')
    # getBankInfo('6113820023998456945')
    error_txt = open(FilePathUtil.create_full_dir("main", "bankcard", "result", "result_bankName_error.txt"), 'a')
    noresult_txt =open(FilePathUtil.create_full_dir("main", "bankcard", "result", "result_bankName_noresult.txt"), 'a')
    exception_txt = open(FilePathUtil.create_full_dir("main", "bankcard", "result", "result_bankName_exception.txt"), 'a')
    file = FilePathUtil.get_full_dir("main", "bankcard", "result", "result_common_bankname.txt")
    f = open(file)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        line = f.readline()
        if line:
            strip = line.strip()
            bankname = strip.split(",")
            if bankname[1]:
                try:
                    info = getBankInfo(bankname[1])
                    # info = unionpay_util.get_card_info(bankname[1])
                    if info['code'] == 0:
                        result_ = info['result']
                        name_ = result_['bank_name']
                        # name_=info['result']
                        isEqual = name_ == bankname[0] or bankname[0] in BankSimplefy.simplefyBankName(name_)
                        print(f"【isTestOK============================={isEqual}======================】")
                        if not isEqual:
                            print(strip, f"接口返回:{name_}",  sep=',',file=error_txt)
                            # print(strip,result_['from_sign'],result_['card_type'], f"接口返回:{name_}",  sep=',',file=error_txt)
                    else:
                        print(strip, sep=',', file=noresult_txt)
                except Exception as e:
                    print(f"{e}")
                    print(strip, f"{e}",sep=',', file=exception_txt)
    f.close()
