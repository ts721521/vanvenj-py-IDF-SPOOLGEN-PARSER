#!/usr/bin/python  
# -*- coding:utf-8 -*-  

import re

def getMtoc(idffile):    
    f = open(idffile,'r')
    s = f.readlines()
    f.close()
    filename = idffile.split('\\')[-1].split('.')[0]
    line = filename + '\n'
    for i in range(s.__len__()):
        tmp = s[i].split(',')
        if tmp.__len__() > 3:
            try :
                tmp = int(tmp[2])
                if tmp >= 1000000:
                    line = line + s[i]
            except :
                pass
    return line

if __name__ == '__main__':
    import glob
    import os
    with open('result.txt', 'w') as fp:
        pass
    for idf in glob.glob(os.getcwd() + '\\*.idf'):
        desc = ''
        desc = getMtoc(idf)
        with open('result.txt', 'a') as fp:
            fp.write(desc)
            
