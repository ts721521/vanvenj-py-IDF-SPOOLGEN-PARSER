#!/usr/bin/python  
# -*- coding:utf-8 -*-  

"""
目的：
    检查客户提供的idf文件是否是真的idf还是仅仅是改了后缀名
    
方法：
    idf 文件包含一些特征值，比如：
    -1 溢出行
    -5 程序名
    -6 管线号
    -20 编码
    -21 描述
    等等
    利用这些特征值大致判断是否是idf文档
"""
import os
import re
import logging
import glob


logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='check.log',
                filemode='w')

#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################


for idf in glob.glob(os.getcwd() + '\\*.idf'):
    input_file = idf
    with open(input_file,'r') as f:
        text = f.read()
        l_1 = re.findall(r'\n\s+-1\s',text)
        l_5 = re.findall(r'\n\s+-5\s',text)
        l_6 = re.findall(r'\n\s+-6\s',text)
        l_20 = re.findall(r'\n\s+-20\s',text)
        l_21 = re.findall(r'\n\s+-21\s',text)
        
        if l_1 and l_5 and l_6 and l_20 and l_21 :
            logging.info(os.path.basename(idf) + '\tis legal idf file')
        else:
            logging.warn(os.path.basename(idf) + '\tis illegal idf file')
    
    
        















    
