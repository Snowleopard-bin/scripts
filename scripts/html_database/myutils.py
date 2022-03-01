#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def clean_chr(s):
    #清洗坏字符
    res = s.replace(':','').replace('\xa0','')
    return res

def is_info(data):
    '''
    判断是否为个人信息
    :param
        data: 待判断的数据
    :return
        True: 个人信息
        False: 检测结果
    '''
    if type(data) == type(()):
        return True
    else:
        return False

def get_child_of_root(root, path):
    '''
    获得路径中根目录的次一级子目录名
    :param
        root: 根目录
    :return
        res: 子目录名
    '''
    if root not in path:
        return None
    from platform import system
    system_version = system()
    dir_list=all_list=[]
    if system_version == "Windows":
        dir_list = root.split('\\')
        all_list = path.split('\\')
    elif system_version == "Linux":
        dir_list = root.split('/')
        all_list = path.split('/')
    else:
        dir_list = root.split('/')
        all_list = path.split('/')
    index = len(dir_list)
    res = all_list[index]
    return res
