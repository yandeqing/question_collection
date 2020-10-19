#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/8/17 16:56
'''
import os
import random
import re

import requests

from main.bankcard import BankSimplefy
from main.common import FilePathUtil, excel_util
from main.common.LogUtil import LogUtil


def cardNum_generator(prefix, length):
    '''
    :param prefix:  银行卡号前几位
    :param length:  银行卡号长度
    :return:
    '''
    cardNum = prefix
    for i in range(length - len(prefix) - 1):
        cardNum = cardNum + str(random.randint(0, 9))
    summation = 0
    for i in range(length):
        if i == 0:
            continue
        tmp1 = int(cardNum[length - i - 1: length - i])
        if (i + 1) % 2 == 0:
            if tmp1 < 5:
                summation = summation + tmp1 * 2
            else:
                tmp2 = str(tmp1 * 2)
                summation = summation + int(tmp2[0]) + int(tmp2[1])
        else:
            summation = summation + tmp1
    check = str(10 - (summation % 10))
    if check == '10':
        check = '0'
    return cardNum + check


def generateBankNumbers(file):
    from stdnum import luhn
    banknums = []
    f = open(file)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        if line:
            try:
                banknum = {}
                arr = line.strip().split(',')
                pattern = re.compile("(\d*)开头的银行卡类型是(.*)")
                res = pattern.search(arr[0]).groups()
                banknum['prefix'] = res[0]
                banknum['bankName'] = BankSimplefy.simplefyBankName(res[1])
                pattern = re.compile("银行卡号数字长度为(\d*)位")
                res = pattern.search(arr[1]).groups()
                banknum['length'] = res[0]
                # print(f'{banknum}')
                num_generator = cardNum_generator(banknum['prefix'], int(banknum['length']))
                banknum['bankNumber'] = num_generator
                valid = luhn.is_valid(num_generator)
                # banknum['luhn_valid'] = valid
                # 校验luhn算法
                # print(f'校验luhn算法是否成功:{valid}')
                banknums.append(banknum)
            except Exception as e:
                LogUtil.info(f"{e}")
        line = f.readline()

    f.close()
    return banknums


def getBankNumbers(file):
    from stdnum import luhn
    banknums = []
    f = open(file, encoding='utf-8')  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        if line:
            try:
                banknum = {}
                arr = line.strip().split(',')
                # 邮储银行,1000000,绿卡银联标准卡,19,6,622188,1
                banknum['prefix'] = arr[5]
                banknum['bankName'] = BankSimplefy.simplefyBankName(arr[0])
                banknum['length'] = arr[3]
                # print(f'{banknum}')
                num_generator = cardNum_generator(banknum['prefix'], int(banknum['length']))
                banknum['bankNumber'] = num_generator
                valid = luhn.is_valid(num_generator)
                # banknum['luhn_valid'] = valid
                # 校验luhn算法
                # print(f'校验luhn算法是否成功:{valid}')
                banknums.append(banknum)
            except Exception as e:
                LogUtil.info(f"{e}")
        line = f.readline()

    f.close()
    return banknums


if __name__ == '__main__':
    numbers = []
    lists = os.listdir('txt')
    for file in lists:
        join = os.path.join("txt", file)
        number = generateBankNumbers(join)
        numbers.extend(number)

    full_dir = FilePathUtil.get_full_dir("main", "bankcard", "bin", "card_bin.txt")
    number = getBankNumbers(full_dir)
    numbers.extend(number)

    zuber_numbers = []
    file = FilePathUtil.get_full_dir("main", "bankcard","result", "zuber_support_bankname.txt")
    f = open(file)  # 返回一个文件对象
    lines = f.readlines()  # 调用文件的 readline()方法
    for line in lines:
        bankname = line.strip()
        if bankname:
            zuber_numbers.append(bankname)
    f.close()

    banks = []
    common_txt = open(
        FilePathUtil.create_full_dir("main", "bankcard", "result", "result_common_bankname.txt"),
        'a')
    all_txt = open(
        FilePathUtil.create_full_dir("main", "bankcard", "result", "result_all_bankname.txt"), 'a')
    for bank in numbers:
        bank_name_ =BankSimplefy.simplefyBankName(bank['bankName'])
        if bank_name_ in zuber_numbers:
            print(bank_name_, bank['bankNumber'], bank['prefix'], sep=',', file=all_txt)
            if bank_name_ not in banks:
                banks.append(bank_name_)
                print(bank_name_, bank['bankNumber'], bank['prefix'], sep=',', file=common_txt)

    common_txt.close()
    all_txt.close()

    # full_dir = FilePathUtil.create_full_dir("main", "bankcard", "xls","kaohaowang_banknumbers.xls")
    # excel_util.write_excel(full_dir, 'banknumbers', numbers_zuber)
    #
    # full_dir = FilePathUtil.create_full_dir("main", "bankcard","xls", "banknumbers.xls")
    # excel_util.write_excel(full_dir, 'banknumbers', numbers)
