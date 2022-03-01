#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import db
import parse
import get_dir_files
import sys,os
import configparser
import myutils

config_file = 'config.ini'
root_dir=''
database_name = ''

def read_config():
    global config_file
    global database_name, root_dir, database_path

    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except Exception as config_err:
        print(config_err)
        print('Configure file: {} cannot found!'.format(config_file))
        sys.exit(-1)
    root_dir = config.get('path','root_dir')
    database_name = config.get('database', 'database_name')
    if not os.path.exists(root_dir):
        print("[Error] 文件夹{} 不存在，请检查config.ini配置文件的root_dir参数".format(root_dir))
        sys.exit(-2)


if __name__ == '__main__':
    
    #Step1: 初始化数据库
    read_config()
    db.dbinit(database_name)

    #Step2: 解析、存入数据
    test = False
    if test:
        html_filepath = './data/20211211/../saved_resource(2).html'
        html_filepath2 = './data/../59_files/saved_resource(2).html'
        result = parse.paresr(html_filepath2)
        print(result)
        db.save_results(result)
    else:
        filenames = get_dir_files.getFiles(root_dir,'.html',targetfile= 'saved_resource(2).html')

        total_result = []
        current_patient = ''
        for filename in filenames:
            print(filename)
            try:
                # 解析网页
                result = parse.paresr(filename)
                total_result.extend(result)
            except Exception as err:
                print(err,filename)

            sub_dir = myutils.get_child_of_root(root_dir, filename)
            if sub_dir and sub_dir != current_patient:  # 判断是否进入另一个病人文件夹
                if current_patient != '':
                    db.save_results(total_result)
                current_patient = sub_dir

        db.save_results(total_result)        

    #Step3：关闭数据库
    db.dbfini()
    input("键入回车键结束...")