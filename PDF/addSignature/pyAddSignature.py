#!/usr/bin/python  
# -*- coding:utf-8 -*-


def mergeSignature(raw,sign,target,x,y):
    from PyPDF2 import PdfFileWriter, PdfFileReader
    '''
    在PDF中插入签名的方法。
       raw:   需要插入签名的pdf文档
      sign:   带签名的pdf文档
    target:   需要输出的pdf文件名
         x:   签名在pdf中的x偏移量
         y:   签名在pdf中的y偏移量
    '''
    output_file = PdfFileWriter()

    #读取签名文件
    f_sign = open(sign,'rb')
    signature_file = PdfFileReader(f_sign)

    #打开需要签名的文件
    with open(raw,'rb') as f_raw:
        input_file = PdfFileReader(f_raw)
        #获取pdf的page数量
        page_count = input_file.getNumPages()
        #对每一个page添加签名
        for page_number in range(page_count):
            input_page = input_file.getPage(page_number)
            input_page.mergeTranslatedPage(signature_file.getPage(0),x,y)
            output_file.addPage(input_page)
        #输出插入签名后的文件
        with open(target,'wb') as outputStream:
            output_file.write(outputStream)            
    #关闭签名文件
    f_sign.close()
    
if __name__ == '__main__':

    #签名文件
    signaturePDF = 'signature.pdf'
    #签名偏移量
    x = -150
    y = -110


    import os
    import glob
    root = os.getcwd()
    input_file_path = root + '\\input_files'
    output_file_path = root + '\\output_files'
    
    if not os.path.exists(input_file_path):
        os.mkdir(input_file_path)        
    if not os.path.exists(output_file_path):
        os.mkdir(output_file_path)
    if not os.path.isfile(root + '\\' + signaturePDF):
        print '签名文件：%s 不存在' % signaturePDF
    else:
        pdfs = glob.glob(root + '\\input_files\\*.pdf')
        n = pdfs.__len__()
        
        for i,pdf in enumerate(pdfs):
            print 'Solving {} of {}...'.format(i + 1,n)
            target = root + '\\output_files\\' + os.path.basename(pdf)
            mergeSignature(pdf,signaturePDF,target,x,y)
    
    
    
    
