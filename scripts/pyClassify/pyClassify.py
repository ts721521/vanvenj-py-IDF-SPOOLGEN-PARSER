# -*- coding=utf8 -*-

import os, shutil

idf_root_folder = './idfs'
pdf_root_folder = './pdfs'
new_pdfs = './new_pdfs/'

#抓取指定目录下所有pdf文件名及其相对路径
pdf_list = []
for path,_,files in os.walk(pdf_root_folder):
    for f in files:
        if '.pdf' in f.lower():
            pdf_list.append([path, f])

#抓取指定目录下所有idf文件名
idf_list = []
for path,_,files in os.walk(idf_root_folder):
    for f in files:
        if '.idf' in f.lower():
            idf_list.append(f)

#配对pdf and idf
pairs = []
for idf in idf_list:
    flag = 0
    for path,pdf in pdf_list:
        if idf.split('.')[0].lower() in pdf.lower():
            pairs.append([idf,path,pdf])
            flag = 1
    if not(flag):
        print idf,'not found pair pdf'

#复制pdf
try:
    shutil.rmtree(new_pdfs)
except:
    pass
finally:
    os.mkdir(new_pdfs)

for _,path,f in pairs:
    shutil.copyfile(path + '/' + f,new_pdfs + f)
