#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
获取目录下的所有文件名
'''
import os

def filter(filename, pattern):
    '''
    过滤后缀
    '''
    if not pattern:
        return True
    if pattern != filename[0-len(pattern):]:
        return False
    return True

def get_files(dir, pattern=None):
    '''
    :param
        dir：目录
        pattern：文件后缀，如'.html'
    :return
        iterator of file path
    '''
    if not os.path.exists(dir):
        raise "目录不存在：" + str(dir)
    
    for parent, dirnames, filenames in os.walk(dir):
        for dirname in dirnames:
            get_files(dirname)
        
        for filename in filenames:
            if not filter(filename, pattern=pattern):
                #过滤 
                continue
            print(dirname,filename)
            yield os.path.join(dir, filename)

'''
#usage:
result = get_files(dir,'.html')
while True:
    file = next(result, None)
    if not file:
        break
    print(file)
'''

def getFiles(dir, suffix, targetfile=None):
    #查找根目录，文件后缀，可指定特定文件名
    res = []
    for root, directory, files in os.walk(dir):
        for filename in files:

            if targetfile:  #只需要目标文件名
                if filename == targetfile:
                    res.append(os.path.join(root, filename))
                continue

            name, suf = os.path.splitext(filename)
            if suf == suffix:
                res.append(os.path.join(root, filename))
    return res