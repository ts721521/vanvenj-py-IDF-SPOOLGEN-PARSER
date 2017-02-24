#!/usr/bin/python  
# -*- coding:utf-8 -*-  

import re


def setMtoCOn(filename):
    """
    PDMS中控制材料是否显示、是否标注使用MTOC控制
    在IDF中以数字的形式标识
    关系如下 ON:0,OFF:1000000,DATU:1100000,DATD:12000000
    此函数通过查找这个值，并且替换成0

    """
    #打开文件，读取整个文件
    f = open(filename,'r')
    s = f.read()
    f.close()
    
    #利用正则表达式替换
    s = re.sub(r"(?<=,\s)1[012]00000(?=\s,)","      0",s)  

    #保存文档
    f = open(filename,'w')
    f.write(s)
    f.close()



if __name__ == '__main__':
    from shutil import copyfile
    import glob
    import os
    for idf in glob.glob(os.getcwd() + '\\*.idf'):
        copyfile(idf,idf + '.bak')    
        setMtoCOn(idf)
