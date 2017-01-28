#!/usr/bin/python  
# -*- coding:utf-8 -*-  

import re

def normalize(filename):

    """
    IDF格式中负数行限制20个字符，这20个字符包含'\n'；
    负数行最后一个字符如果是空格，那么这行就只有19个字符,需要补一个空格；
    -1行表示溢出行，这行信息属于上一行；
    需要利用正则表达式处理这个问题。
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

if __name__ == '__main__':
    tmp = normalize('test.idf')
    print tmp
        
    
