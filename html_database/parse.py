#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import etree
import myutils

def experimental_result_func(html, properties_class, tmp_project, tmp_result, value_index=1):
    i=1
    while True:
        properties_project = '//td[@class="'+ properties_class +'"]/../following-sibling::*['+ str(i) +']//nobr/text()'    #项目下黑线第n行
        result_list = html.xpath(properties_project)
        i+=1
        if result_list != []:
            if '建议' in result_list[0] or '检验者' in result_list[0] or '评价' in result_list[0]:
                break
            if '(' in result_list[0] and ')' not in result_list[0]: # 分为两行
                tmp_project.append(result_list[0]+result_list[1])
                tmp_result.append(result_list[value_index+1])
            else:
                tmp_project.append(result_list[0])
                tmp_result.append(result_list[value_index])
        if i > 100:
            return False
    return True

def paresr(html_filepath):
    '''
    表达式 	描述
    nodename 	选取此节点的所有子节点
    / 	从当前节点选取直接子节点
    // 	从当前节点选取子孙节点
    . 	选取当前节点
    .. 	选取当前节点的父节点
    @ 	选取属性
    * 	通配符，选择所有元素节点与元素名
    @* 	选取所有属性
    [@attrib] 	选取具有给定属性的所有元素
    [@attrib='value'] 	选取给定属性具有给定值的所有元素
    [tag] 	选取所有具有指定元素的直接子节点
    [tag='text'] 	选取所有具有指定元素并且文本内容是text节点
    '''
    '''
    #方案一
    html = etree.parse(html_filepath,etree.HTMLParser())
    properties_start = '//td[@class="cs99E26756"]/../following-sibling::*//nobr/text()'  #上黑线之后
    result = html.xpath(properties_start)

    # properties_end = '//td[@class="csBD220B90"]/../following-sibling::*//nobr/text()'    #下黑线之前
    # num = len(html.xpath(properties_end))
    # if len(result) > 1:
    #     result = result[:-1-num]

    # html = etree.parse(html_filepath,etree.HTMLParser())
    # properties_info = '//td[@class="csC9D58A34"]/../preceding-sibling::*//nobr/text()'  #上黑线之后第5个值 有重复class
    # project = html.xpath(properties_info)
    # return project
    '''
    
    #方案二
    html = etree.parse(html_filepath,etree.HTMLParser())
    project = []
    result = []
    tmp_project = []
    tmp_result = []
    #病人信息
    # properties_info = '//img[@src="./ReportView.aspx"]/../../../preceding-sibling::*//td[4]/nobr/text() | //img[@src="./ReportView.aspx"]/../../../preceding-sibling::*//td[8]/nobr/text() | //img[@src="./ReportView.aspx"]/../../../preceding-sibling::*//td[16]/nobr/text() | //img[@src="./ReportView.aspx"]/../../../preceding-sibling::*//td[22]/nobr/text()' #一维码图片以前 4,8,16,22
    # project1 = html.xpath(properties_info)[:4]
    # properties_result = '//img[@src="./ReportView.aspx"]/../../../preceding-sibling::*//td[6]/nobr/text() | //img[@src="./ReportView.aspx"]/../../../preceding-sibling::*//td[9]/nobr/text() | //img[@src="./ReportView.aspx"]/../../../preceding-sibling::*//td[18]/nobr/text() | //img[@src="./ReportView.aspx"]/../../../preceding-sibling::*//td[24]/nobr/text()' #一维码图片以前 6,9,18,24
    # result1 = html.xpath(properties_result)[:4]
    properties_info = '//td[@class="csC9D58A34"]/../following-sibling::*[3]//nobr/text()'   #黑线第3行
    info = html.xpath(properties_info)
    project1 = list(map(myutils.clean_chr, info[::2]))
    result1 = info[1::2]
    project += project1
    result += result1

    #检测结果
    experimental_result = experimental_result_func(html, "cs99E26756", tmp_project, tmp_result)
    
    #采样时间 + 另类报告单
    # properties_time = '//td[@style="width:127px;height:18px;line-height:13px;text-align:left;vertical-align:middle;"]//nobr/text()' #属性值唯一？NO
    # properties_time = '//td[@class="csC9D58A34"]/../preceding-sibling::*[4]//nobr/text()'   #不同报告单class不一致
    # result3 = html.xpath(properties_time)#[-1].replace('\xa0',' ')
    # if result3 != []:
    #     result3 = html.xpath(properties_time)[-1].replace('\xa0',' ')
    # else:
    #     properties_time = '//td[@class="csA5ABC6A0"]/../preceding-sibling::*[8]//nobr/text()'
    #     result3 = html.xpath(properties_time)
    #     if result3 != []:
    #         result3 = html.xpath(properties_time)[-1].replace('\xa0',' ')
    j=1
    sample_time=''
    last_value = ''
    first_project = ''
    sensitivity_flag = False    # 是否为药敏报告单
    bacteriaName_flag = False   # 检测到菌名
    bacteriaName = ''
    while True:
        #properties_project = '//td[@class="csC9D58A34"]/../following-sibling::*['+ str(j) +']//nobr/text()'    #项目下黑线第n行
        properties_time = '//img[@src="./ReportView.aspx"]/../../../following-sibling::*['+ str(j) +']//nobr/text()'
        result_list = html.xpath(properties_time)
        j+=1
        if len(result_list)>2:
            if '采样时间' in result_list[-2]:
                sample_time = result_list[-1].replace('\xa0',' ')
                if experimental_result: # 检测结果已提取完毕
                    break
        if not experimental_result and result_list!=[]: # 检测结果异常，提取检验组合+仪器名称/检验组合+菌名 和 检测结果
            if '检验组合' in result_list[0]:
                first_project = last_value
                continue
            if '仪器名称' in result_list[0] and not sensitivity_flag:   # 药敏不提取仪器名称
                first_project += '_' + result_list[1]
                tmp_project.append(first_project)
                continue
            if sensitivity_flag and '菌名' in myutils.clean_chr(result_list[0]):
                bacteriaName_flag = True
                continue
            if '建议' in result_list[0] or '检验者' in result_list[0] or '评价' in result_list[0]:
                tmp_result.append(last_value)
                break

        if result_list:
            if len(result_list[0])>0:
                last_value = result_list[0]
                if '药敏' in last_value:
                    sensitivity_flag = True # 标记药敏报告单
                if bacteriaName_flag:   # 检测到菌名后下一条数据
                    bacteriaName = last_value
                    first_project += '_' + bacteriaName
                    tmp_project.append(first_project)
                    tmp_result.append('sensitivity')
                    break

    experimental_result = experimental_result_func(html, "cs1FD3F985", tmp_project, tmp_result, value_index=2)  # 取第二个值为敏感度

    tmp_project.append('采样时间')
    tmp_result.append(sample_time)   
    tmp = list(zip(tmp_project, tmp_result))
    report = list(zip(project,result))
    report.append(tmp)
    return report

