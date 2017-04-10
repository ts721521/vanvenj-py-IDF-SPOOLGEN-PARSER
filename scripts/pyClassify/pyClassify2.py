# -*- coding=utf8 -*-

import os, shutil, re

"""
提取不同文件夹中所有idf目录清单，同时提取最新版
文件名格式如下：
abcde_C1.idf    1版
abcde_C2.idf    2版
abcde.idf          0版
"""

idf_root_folder = './idfs'
new_idfs = './new_idfs/'

#抓取指定目录下所有idf文件名及其相对路径
idf_list = []
for path,_,files in os.walk(idf_root_folder):
    for f in files:
        if '.idf' in f.lower():
            #获取版次
            m = re.search(r'(?<=_C)\d{1,}',f)
            #匹配_C开始的数字
            if m:
                rev = int(m.group(0))
            else:
                rev = 0
            #print rev,type(rev)

            #获取管线号
            m = re.search(r'.*(?=_C)',f)
            if m:
                line = m.group(0)
            else:
                line = f.split('.')[0]
            
            idf_list.append((path, line, rev, f))

#对idf_list 按管线号，版次排序
idf_list = sorted(idf_list,key=lambda(path,line,ver,f):(line,ver))
#提取管线号清单，并且去重
line_list = set(map(lambda x:x[1], idf_list))
#对idf按管线分组存放不同版次
idf_group = [[y for y in idf_list if y[1]==x] for x in line_list]



with open('idf_list.txt.xls','w') as f:
    for l in idf_list:
        a,b,c,d = l
        f.write(a + '\t' + b + '\t' + str(c) + '\t' + d + '\n')
    


#复制pdf
try:
    shutil.rmtree(new_idfs)
except:
    pass
finally:
    os.mkdir(new_idfs)

for i in idf_group:
    f =  i[-1]
    shutil.copyfile(f[0] + '/' + f[3],new_idfs + f[3])
