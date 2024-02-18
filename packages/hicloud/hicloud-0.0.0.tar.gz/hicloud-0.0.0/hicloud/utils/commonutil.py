#!/usr/bin/python
# -*- coding:UTF-8 -*-

import os, sys


# 打印文件所在位置
def get_path():
    return os.path


# 获取python的版本信息
def get_py_version():
    return sys.version


# 返回操作系统平台的名称
def get_sys_platform():
    return sys.platform


# 退出程序，正常退出是exit(0)
# def exit(code):
#     sys.exit(code)


# if __name__ == '__main__':
    # print(get_py_version())
    # print(get_sys_platform())
