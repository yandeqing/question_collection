#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/8/17 16:56
'''
import json
import os
import re

from main.bankcard import BankSimplefy
from main.common import FilePathUtil, excel_util
from main.common.LogUtil import LogUtil


def classfy_bank():
    full_dir = FilePathUtil.get_full_dir("main", "bankcard", "bin", "card_bin.txt")
    path = "classify_bankname.txt"
    if os.path.exists(path):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(path)
    txt = open(path, 'w')
    f = open(full_dir, encoding='utf-8')
    line = f.readline()
    banknames = []
    while line:
        line = f.readline()
        if line:
            try:
                arr = line.strip().split(',')
                if arr[0] not in banknames:
                    banknames.append(arr[0])
                    print(arr[0], file=txt)
                    print(f'{arr[0]}')
                txt.close()
            except Exception as e:
                LogUtil.info(f"{e}")
    f.close()
    return banknames






if __name__ == '__main__':
    # print(f"【main().array=共计{len(classfy_bank())}家银行】")
    zuber_banks = BankSimplefy.get_bankinfo()
    f = open(FilePathUtil.get_full_dir("main", "bankcard", "result", "result_common_bankname.txt"))  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    bankinfos=[]
    while line:
        if line:
            strip = line.strip()
            bankname = strip.split(",")
            bankinfos.append(bankname[0])
        line = f.readline()
    path =FilePathUtil.create_full_dir("main", "bankcard", "result","no_common_bankname.txt")
    txt = open(path, 'w')
    no_commons=[]
    for l in zuber_banks:
        if l not in bankinfos:
            no_commons.append(l)
            print(l,file=txt)
    txt.close()
    print(f"【main().array=共计{len(no_commons)}家】")
