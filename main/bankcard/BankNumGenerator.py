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
        line = f.readline()
        if line:
            try:
                banknum = {}
                arr = line.strip().split(',')
                pattern = re.compile("(\d*)开头的银行卡类型是(.*)")
                res = pattern.search(arr[0]).groups()
                banknum['prefix'] = res[0]
                banknum['bankName'] = res[1]
                pattern = re.compile("银行卡号数字长度为(\d*)位")
                res = pattern.search(arr[1]).groups()
                banknum['length'] = res[0]
                print(f'{banknum}')
                num_generator = cardNum_generator(banknum['prefix'], int(banknum['length']))
                banknum['bankNumber'] = num_generator
                valid = luhn.is_valid(num_generator)
                # banknum['luhn_valid'] = valid
                # 校验luhn算法
                print(f'校验luhn算法是否成功:{valid}')
                try:
                    url = f'http://elklog.zuker.im/bankcard/?area=false&card_id={num_generator}'
                    print(url)
                    result = requests.get(url)
                    json = result.json()
                    if json['code'] is 0:
                        if json['result']:
                            banknum = {**banknum, **json['result']}
                            print(f'{banknum}')
                            banknums.append(banknum)
                        else:
                            LogUtil.info(f'{banknum}')
                            txt = open("error_banknumber.txt", 'a')
                            print(banknum['prefix'], num_generator, banknum['bankName'], sep=',',
                                  file=txt)
                            txt.close()
                    else:
                        LogUtil.info(f'{banknum}')
                        txt = open("error_banknumber.txt", 'a')
                        print(banknum['prefix'],num_generator,banknum['bankName'],sep=',',  file=txt)
                        txt.close()
                except Exception as e:
                    print(f"{e}")
            except Exception as e:
                LogUtil.info(f"{e}")

    f.close()
    return banknums


if __name__ == '__main__':

    numbers = []
    lists = os.listdir('txt')
    for file in lists:
        join = os.path.join("txt", file)
        number = generateBankNumbers(join)
        numbers.extend(number)
        print(numbers)

    full_dir = FilePathUtil.get_full_dir("main", "bankcard", "banknumbers.xls")
    excel_util.write_excel(full_dir, 'banknumbers', numbers)
    # os.system(full_dir)
