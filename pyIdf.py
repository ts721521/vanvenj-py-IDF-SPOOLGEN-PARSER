#!/usr/bin/python  
# -*- coding:utf-8 -*-  

import re
import math

def normalize(filename):

    """
    IDF格式中负数行限制20个字符，这20个字符包含'\n'；
    负数行最后一个字符如果是空格，那么这行就只有19个字符,需要补一个空格；
    -1行表示溢出行，这行信息属于上一行；
    需要利用正则表达式的sub函数处理这些问题。
    example:
      -20 AAGAARBJJAA
      -21 ASME B16.21 N
       -1 on-metal flan
       -1 ge Gasket RF
       -1 CL150
    -9920 PTS2S4AW80495
      -21 95 Stud Bolt
       -1 5/8-11UNC B18
       -1 .31.2 A193 GR
       -1  B8 CL2 W-B18
       -1 .2.2 A194GR.8
       -1  UNTS@
    """
    f = open(filename,'r')
    text = f.read()
    f.close()

    #对负数行执行左对齐，用空格在右侧补齐20个字符
    negativeLinePattern = re.compile(r'\n\s*-\d+\s.+?(?=\n)')
    text = negativeLinePattern.sub((lambda m:m.group(0).ljust(20)),text)

    #将负一行合并到上一行，通过替换掉-1头部，保留第二部分描述部分。
    overFlowTextPattern = re.compile(r'(\n\s+-1\s)(.+?)(?=\n)')
    text = overFlowTextPattern.sub(r'\2',text)

    #去除负数行尾部多余空格,第一分组中文号为启用非贪婪模式
    negativeLineSpacePattern = re.compile(r'(\n\s*-\d+\s.+?)(\s+)(?=\n)')
    text = negativeLineSpacePattern.sub(r'\1',text)
    return text

def getMaterialList(content):
    """
    idf的一些标识符及对应的含义:
    -6 管线号
    -8 版次
   -10 模块信息
   -11 技术等级
   -12 压力等级
   -13 Line Type
   -14 创建日期
   -20 物料编码
   -21 物料描述
   -22 位号
   -30 Conn on
   -37 用户自定义信息(ATTA)
   -39 Unique Component Identifier

    30 BEND
    35 ELBOW
    40 OLET
    45 TEE
    50 CROSS
    55 REDU
    60 TEE
    65 FLAN
    70 ELBO
    75 VALV
    80 VALV
    85 VALV
    90 INST
    95 PCOM
   100 PIPE
   101 PIPE
   102 PIPE
   103 PIPE
   105 FLAN
   106 STUB
   107 BLIND
   110 GASK
   115 BOLT
   120 WELD
   125 CAP
   126 COUP
   127 UNION
   130 VALV
   132 TRAP
   134 VENT
   136 FILT
   149 ATTA 备注
   150 PS
    
    """
    #构造材料清单数据结构
    #管线信息
    lineInfo = {'lineNo':'','rev':'','moduleNo':'','createTime':''}
    #材料明细
    materialDict = {'rowNo':'','record':'','ea':1,'mm':'','mtoc':'','ref':'','partNo':'','tag':'','size1':'','size2':''}
    materialList = []
    #材料编码、描述
    materialCodeDict = {'code':'','desc':''}
    materialCodeList = ['']
    #材料明细特征值
    componentRecord = [30,35,40,45,50,55,60,65,70,75,
                       80,85,90,95,100,101,102,103,105,
                       106,107,110,115,125,126,127,
                       130,132,134,136,150]
    #带分支的特征值
    #componentRecordWithSecondBranch = [41,46,51,61,81,86,91]
    lines = content.split('\n')
    #遍历IDF文档，将文档转换成材料清单与物料编码描述对照表,并且合并
    for row,line in enumerate(lines):
        try:
            IsogenRecord = int(line[0:5])
            #提取管线号
            if IsogenRecord == -6:
                lineInfo['lineNo'] = line[6:]
            #提取版次
            elif IsogenRecord == -8:
                lineInfo['rev'] = line[6:]
            #提取模块号
            elif IsogenRecord == -10:
                lineInfo['moduleNo'] = line[6:]
            #提取创建时间
            elif IsogenRecord == -14:
                lineInfo['createTime'] = line[6:]
            #提取元件信息
            elif IsogenRecord in componentRecord:
                #必须使用dict(materialDict)或者materialDict.copy()创建一个新的dict，否则都是一样的
                materialList.append(dict(materialDict))
                materialList[-1]['rowNo'] = row + 1
                materialList[-1]['record'] = IsogenRecord
                materialList[-1]['mtoc'] = int(line.split(',')[2])
                materialList[-1]['partNo'] = int(line[82:86])
                materialList[-1]['size1'] = int(line[72:78])
                #提取管子长度
                if IsogenRecord == 100:
                    x1,y1,z1,x2,y2,z2 = map(int,re.split('\s+',line[7:72].strip()))
                    materialList[-1]['mm'] = math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
            elif IsogenRecord == -22:
                materialList[-1]['tag'] = line[6:]
            elif IsogenRecord == 41:
                materialList[-1]['size2'] = int(line[72:78])
                materialList[-1]['partNo'] = int(line[82:86]) #olet分支上一个件号不准
            elif IsogenRecord in [46,51,61,81,86,91]:
                materialList[-1]['size2'] = int(line[72:78])         
            
            #提取并设定列表的最后一个字典的ref属性
            elif IsogenRecord == -39:
                materialList[-1]['ref'] = line[6:]
            elif IsogenRecord == -20:
                materialCodeList.append(dict(materialCodeDict))
                materialCodeList[-1]['code'] = line[6:]
            elif IsogenRecord == -21:
                materialCodeList[-1]['desc'] = line[6:]                       
            else:
                pass

        except ValueError as e:
            #print str(e)
            pass

    materialFullList = mergeMaterialList(materialList,materialCodeList)    
    return lineInfo,materialFullList

def mergeMaterialList(materialList,materialCodeList):
    """
    将材料清单内容扩充
    通过材料清单中的件号去物料编码表中索引
    最后更新到材料清单中
    """
    for i,line in enumerate(materialList):
        materialList[i].update(materialCodeList[materialList[i]['partNo']])
    #print materialList
    return materialList


    

if __name__ == '__main__':
    #创建带标题的空文件
    f = open('list.txt','w')
    headlist = ['lineNo','rev','moduleNo','createTime','rowNo','record','ea','mm','mtoc','ref','partNo','code','size1','size2','desc','tag']
    head = ''
    for i in headlist:
        head = head + i + '\t'
    head = head + '\n'
    f.write(head)
    f.close()

    #使用glob与os处理当前文件夹下所有idf文档
    import os
    import glob
    for idf in glob.glob(os.getcwd() + '\\*.idf'):
        print "Solving : " +  idf
        f = open('list.txt','a')
        tmp = normalize(idf)    
        lineInfo,materialList = getMaterialList(tmp)
        newline = ''
        for line in materialList:
            #print line
            for i in headlist[0:4]:        
                newline = newline + str(lineInfo[i]) + '\t'
            for i in headlist[4:]:
                newline = newline + str(line[i]) + '\t'
            newline = newline + '\n'
        f.write(newline)
        f.close()
        















    
