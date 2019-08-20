#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/8/17 16:56
'''
import random
import re


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


if __name__ == '__main__':
    from stdnum import luhn
    f = open("txt/abc_bank_text.txt")  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        line = f.readline()
        if line:
            banknum={}
            arr = line.strip().split(' ')
            pattern = re.compile("(\d*)开头的银行卡是(.*)")
            res = pattern.search(arr[0]).groups()
            banknum['prefix']=res[0]
            banknum['bankName']=res[1]
            pattern = re.compile("银行卡号数字长度为(\d*)位")
            res = pattern.search(arr[1]).groups()
            banknum['length']=res[0]
            num_generator = cardNum_generator("6226", 19)
            banknum['bankNumber'] = num_generator
            valid = luhn.is_valid(num_generator)
            banknum['luhn_valid'] = valid
            # 校验luhn算法
            print(f'校验luhn算法是否成功:{valid}')
            print(f'{banknum}')

    f.close()
