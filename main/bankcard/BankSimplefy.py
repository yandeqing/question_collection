#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/8/17 16:56
'''
import os
import re

from main.common import FilePathUtil, excel_util


def get_bankinfo():
    full_dir = FilePathUtil.get_full_dir("main", "bankcard", "xls", "id_bankname.xls")
    arrays = excel_util.excel2array(full_dir, "Sheet1")
    banknames = []
    path = FilePathUtil.create_full_dir("main", "bankcard", "result", "zuber_support_bankname.txt")
    txt = open(path, 'w')
    for name in arrays:
        name_ = name['参与者别名']
        bank_name = simplefyBankName(name_)
        if bank_name == '农村信用社':
            bank_name = name['参与者名称']
        if bank_name not in banknames:
            banknames.append(bank_name)
            bank_name = trim_bankname(bank_name)
            print(bank_name, file=txt)
        print(f"【complete_bankinfo().name={bank_name}】")
    txt.close()
    return banknames


def trim_bankname(bank_name):
    for bank in CONST_ARRAY:
        if bank_name in bank.keys():
            bank_name = bank.get(bank_name)
    for bank in REPLACE_ARRAY:
        for key in bank.keys():
            if key in bank_name:
                bank_name = bank_name.replace(key, bank.get(key))
    return bank_name


CONST_ARRAY = []
CONST_ARRAY.append({'农业银行': "中国农业银行"})
CONST_ARRAY.append({'工商银行': "中国工商银行"})
CONST_ARRAY.append({'民生银行': "中国民生银行"})
CONST_ARRAY.append({'农业银行': "中国农业银行"})
CONST_ARRAY.append({'浦发银行': "上海浦东发展银行"})
CONST_ARRAY.append({'浦东发展银行': "上海浦东发展银行"})
CONST_ARRAY.append({'邮政储蓄银行': "中国邮政储蓄银行"})
CONST_ARRAY.append({'邮储银行': "中国邮政储蓄银行"})
# CONST_ARRAY.append({'广发银行': "广东发展银行"})

REPLACE_ARRAY = []
REPLACE_ARRAY.append({'农村信用联合社': "农村信用社"})
REPLACE_ARRAY.append({'农村信用社联合社': "农村信用社"})
REPLACE_ARRAY.append({'农商银行': "农村商业银行"})
REPLACE_ARRAY.append({'农信': "农村信用社"})
REPLACE_ARRAY.append({'省': ""})
REPLACE_ARRAY.append({'市': ""})


def simplefyBankName(bankName):
    re_compile = re.compile("(.*?)农村信用社")
    compile_search = re_compile.search(bankName)
    if compile_search:
        groups = compile_search.groups()
        if groups:
            if len(groups[0]):
                name_simple = groups[0] + "农村信用社"
            else:
                name_simple = bankName
        else:
            name_simple = bankName
    else:
        pattern = re.compile("(.*?)银行")
        search = pattern.search(bankName)
        if search:
            groups = search.groups()
            if groups:
                name_simple = groups[0] + "银行"
            else:
                name_simple = bankName
        else:
            name_simple = bankName
    return trim_bankname(name_simple)


if __name__ == '__main__':
    # name = get_bankinfo()
    bankname = simplefyBankName('民生银行民生国际卡借记卡')
    print(f"【main().bankname={bankname}】")
