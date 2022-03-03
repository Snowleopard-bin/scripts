#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import time
import myutils
from re import sub
conn = '' 
cursor = ''

def dbinit(database_name):
    global conn, cursor
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
def dbfini():
    global conn
    conn.close()

def drop_all_tables():
    global cursor
    sql = 'select name from sqlite_master;'
    cursor.execute(sql)
    result = cursor.fetchall()
    
    for table in result:
        table_name = table[0]
        drop_sql = 'drop table {};'.format(table_name)
        cursor.execute(drop_sql)

def timeformat(day):
    day = day.replace('/','-')
    tmp = time.strptime(day,"%Y-%m-%d %H:%M:%S")
    result = time.strftime("%Y-%m-%d %H:%M:%S",tmp)
    return result

def waf(sql):
    sql = sub('[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\xa0]+', '_', sql)
    result = sql.replace('(','').replace(')','').replace('-','_').replace('.','_').replace('%','').replace('+','_').replace('/','_').replace(' ','_')
    return result

def create_table(table_name, property):
    '''
    创建新表
    :param
        table_name: 表名
        property: 属性名
    '''
    global cursor, conn
    property = waf(property)
    table_name = waf(table_name)
    create = '''create table {}(
    名字 TEXT NOT NULL,
    性别 CHAR(4),
    年龄 INT,
    住院号 INT,
    门诊号 INT,
    {} TEXT,
    Time date,
    primary key (住院号,门诊号,{},Time)
    );'''.format(table_name, property, property)

    cursor.execute(create)
    conn.commit()

def create_table_sensitivity(table_name):
    '''
    创建新表
    :param
        table_name: 表名
        property: 属性名
    '''
    global cursor, conn
    table_name = waf(table_name)
    create = '''create table {}(
    名字 TEXT NOT NULL,
    性别 CHAR(4),
    年龄 INT,
    住院号 INT,
    门诊号 INT,
    检验组合_菌名 TEXT,
    敏感度 TEXT,
    Time date,
    primary key (住院号,门诊号,检验组合_菌名,敏感度,Time)
    );'''.format(table_name)

    cursor.execute(create)
    conn.commit()

def insert_table(table_name, name, sex, age, inpatient_num, outpatient_num, value, day):
    '''
    插入数据
    :param
        table_name: 表名
        name: 名字
        sex: 性别
        age: 年龄
        inpatient_num: 住院号
        outpatient_num: 门诊号
        value: 检测结果
        day: 采样时间
    '''
    global cursor, conn
    day = timeformat(day)
    table_name = waf(table_name)
    insert = ''' insert or ignore into {} values ("{}", "{}", "{}", "{}", "{}", "{}", "{}");'''.format(table_name, name, sex, age, inpatient_num, outpatient_num, value, day)
    cursor.execute(insert)
    conn.commit()

def insert_table_sensitivity(table_name, name, sex, age, inpatient_num, outpatient_num, value, sensitivity, day):
    '''
    插入数据
    :param
        table_name: 表名
        name: 名字
        sex: 性别
        age: 年龄
        inpatient_num: 住院号
        outpatient_num: 门诊号
        value: 检测组合_菌名
        sensitivity: 敏感度
        day: 采样时间
    '''
    global cursor, conn
    day = timeformat(day)
    table_name = waf(table_name)
    insert = ''' insert or ignore into {} values ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");'''.format(table_name, name, sex, age, inpatient_num, outpatient_num, value, sensitivity, day)
    cursor.execute(insert)
    conn.commit()

def queryall(sql):
    global cursor, conn
    sql = waf(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result
    
def query_table(table_name):
    '''
    检查是否存在table
    :param
        table_name: 表名
    :return
        1: 存在
        0: 不存在
    '''
    global cursor
    table_name = waf(table_name)
    table_sql = "select count(*) from sqlite_master where type='table' and name='{}';".format(table_name)
    cursor.execute(table_sql)
    result = cursor.fetchall()
    return result[0][0]

def save_info(values, info):
    '''
    将个人信息写入字典
    :param
        values: 字典
        info: 元组(项目, 值)
    '''
    index, value = info
    if '姓名' in index :
        values['姓名'] = value
    elif '性别' in index :
        values['性别'] = value
    elif '年龄' in index :
        values['年龄'] = value
    elif '住院号' in index :
        values['住院号'] = value
    elif '门诊号' in index :
        values['门诊号'] = value    

def save_results(result_list):
    '''
    将病人完整的检测数据录入数据库
    :param
        result_list: 检测数据列表
    :return
        1: 成功
        0: 失败
    '''
    global cursor
    values = {'姓名':'', '性别':'', '年龄':None, '住院号':None, '门诊号':None, 'Time':None}

    for result in result_list:
        if myutils.is_info(result): # 个人信息
            save_info(values, result)
        else:
            time = result[-1][1]
            bacteriaName=None
            for project in result:  # 检测数据
                index, value = project
                index = waf(index)
                if index == '采样时间':
                    break
                if value == 'sensitivity':
                    bacteriaName = index
                    continue
                if bacteriaName:
                    if query_table(index) == 0:  # 表未创建
                        create_table_sensitivity(index)  #表名 = 项目
                    insert_table_sensitivity(index, values['姓名'], values['性别'], values['年龄'], values['住院号'], values['门诊号'], bacteriaName, value, time)
                else:
                    if query_table(index) == 0:  # 表未创建
                        create_table(index, index)  #表名 = 项目
                    insert_table(index, values['姓名'], values['性别'], values['年龄'], values['住院号'], values['门诊号'], value, time)
                

# if __name__ == '__main__':
#     dbinit('patient.db')

#     drop_all_tables()

#     dbfini()
