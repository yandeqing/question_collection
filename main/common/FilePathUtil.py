#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/5/16 14:36
'''
import os

currentFile = os.path.split(os.path.realpath(__file__))[0]
proDir = currentFile[:currentFile.find("question_collection\\") + len("question_collection\\")]


def getProjectRootDir():
    return proDir


def get_full_dir(path, *paths):
    return os.path.join(proDir, path, *paths)


def get_lastmodify_file(test_report):
    if os.path.isdir(test_report):
        lists = os.listdir(test_report)
        lists.sort(key=lambda fn: os.path.getmtime(test_report + os.path.sep + fn))
        if len(lists) > 0:
            return get_lastmodify_file(os.path.join(test_report, lists[-1]))
        else:
            return test_report
    else:
        return test_report


def del_file(path):
    try:
        if os.path.isfile(path):
            if os.path.exists(path):
                os.remove(path)
        else:
            ls = os.listdir(path)
            for i in ls:
                c_path = os.path.join(path, i)
                del_file(c_path)
    except:
        pass


def getstringfromfile(filepath):
    content = None
    try:
        file = open(filepath, "r", encoding='utf-8')
        content = file.read()
        file.close()
    except Exception as e:
        print(f"{e}")
    return content
