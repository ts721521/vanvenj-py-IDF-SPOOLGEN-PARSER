# -*- coding:utf-8 -*-

from __future__ import division 


def is_solved_by_ms_excel(file_name):    
    """
    检查原始文件是否被Excel处理过
    """
    try:
        with open(file_name,'r') as f:
            txt = f.read()
            if '""' in txt and '\t' in txt:
                logging.warn(file_name + ' has been solved by MS Excel!')
                return True
            else:
                logging.info(file_name + ' is Raw.')
                return False
    except Exception,e:
        logging.warn(e)



def file_to_list(file_name,file_index):
    """
    将文件根据索引数据转换成数组
    """
    file_index.sort() # index排序
    file_index = [i - 1 for i in file_index] # index 索引从1改成0
    file_index = map(None,file_index,file_index[1:]) # 制作索引元组
    data_return = []
    with open(file_name,'r') as f:
        for l in f:
            data_return.append([l[i[0]:i[1]].strip() for i in file_index])
    return data_return

def file_to_list2(file_name,file_index):
    """
    被Excel处理过得原始文件
    """
    data_return = []
    with open(file_name,'r') as f:
        for l in f:
            data_return.append(l.strip().split('\t'))
    return data_return    

def write_to_excel(file_name,data):
    """
    输出Excel
    """
    import logging
    wb = Workbook()
    ws = wb.active
    for d in data:
        ws.append(d)
    try:
        wb.save(file_name)
    except Exception,e:
        logging.warn(e)     


def fraction_to_decimal(string):
    """
    将尺寸分数转换成数字
    """
    return eval(re.sub(r'[\s\.]','+',string))

if __name__ == '__main__':

    import os
    import re
    import logging
    import collections
    from ConfigParser import ConfigParser
    from openpyxl import Workbook
    from glob import glob    

    '''
    Level Numeric value 
    CRITICAL 50 
    ERROR 40 
    WARNING 30 
    INFO 20 
    DEBUG 10 
    NOTSET 0 
    '''
    # 配置日志级别
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='imes.log',
                    filemode='a')
    #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)    

    # 加载用户自定义信息
    config = ConfigParser()
    config.read('conf.ini')
    user_params = config._sections['user_define']    
    module_name = user_params['module_name']
    module_path = user_params['module_path']
    sub_folder_name = user_params['sub_folder_name']
    workorder_no = user_params['workorder_no']
    raw_cutting_list_for_bom=user_params['raw_cutting_list_for_bom']
    raw_material_list_for_bom=user_params['raw_material_list_for_bom']
    raw_material_list_for_imes=user_params['raw_material_list_for_imes']
    raw_welding_list_for_imes=user_params['raw_welding_list_for_imes']    
    raw_cutting_list_for_bom_index=user_params['raw_cutting_list_for_bom_index']
    raw_material_list_for_bom_index=user_params['raw_material_list_for_bom_index']
    raw_material_list_for_imes_index=user_params['raw_material_list_for_imes_index']
    raw_welding_list_for_imes_index=user_params['raw_welding_list_for_imes_index']
    raw_file = [raw_cutting_list_for_bom,raw_material_list_for_bom,
                raw_material_list_for_imes,raw_welding_list_for_imes ]
    # 处理用户信息
    # 利用正则表达式处理用户输入的不确定符号
    # 比如:全角、半角、逗号、空格、tab
    module_name = re.split(r'[，\s\t,]{1,}',module_name)    
    module_path = module_path.rstrip('\\') + '\\'
    sub_folder_name = sub_folder_name.strip('\\') + '\\' if sub_folder_name else ''
    raw_cutting_list_for_bom_index=[int(n) for n in re.split(r'[，\s\t,]{1,}',raw_cutting_list_for_bom_index)]
    raw_material_list_for_bom_index=[int(n) for n in re.split(r'[，\s\t,]{1,}',raw_material_list_for_bom_index)]
    raw_material_list_for_imes_index=[int(n) for n in re.split(r'[，\s\t,]{1,}',raw_material_list_for_imes_index)]
    raw_welding_list_for_imes_index=[int(n) for n in re.split(r'[，\s\t,]{1,}',raw_welding_list_for_imes_index)]
    raw_cutting_list_for_bom_index.sort(key=int)
    raw_material_list_for_bom_index.sort(key=int)
    raw_material_list_for_imes_index.sort(key=int)
    raw_welding_list_for_imes_index.sort(key=int)
    
##    print raw_cutting_list_for_bom_index
##    print raw_material_list_for_bom_index
##    print raw_material_list_for_imes_index
##    print raw_welding_list_for_imes_index

    # 检查原始文件是否被Excel处理过，如果有处理过，退出程序
    excel_solved_flag = 0
    for m in module_name:
        for f in raw_file:
            f_name = module_path + m + '\\' +  sub_folder_name + f
            if is_solved_by_ms_excel(f_name):
                excel_solved_flag = 1
                
    if excel_solved_flag:
        logging.warn('原始文件有问题，请检查日志')
    else:
        #BOM
        bom = [['line_no','spool_no','group','code','quantity','unit','type','desc']]
        for m in module_name:
            f_cutting_list = module_path + m + '\\' +  sub_folder_name + raw_cutting_list_for_bom
            f_material_list = module_path + m + '\\' +  sub_folder_name + raw_material_list_for_bom
            
            pipes = file_to_list(f_cutting_list,raw_cutting_list_for_bom_index)
            for pipe in pipes:
                if not('---' in pipe[0] ):
                    bom.append([pipe[0], pipe[0] + '_' + pipe[6], 'PIPE', pipe[4], int(pipe[2]) / 1000.0, 'm', 'FAB', pipe[8]])
                    
            fittings = file_to_list(f_material_list,raw_material_list_for_bom_index)
            for fit in fittings:
                if not('---' in fit[0] or fit[5] == 'PIPE'):
                    if fit[5] == 'SUPPORTS':
                        #sini 支架编码有问题，需要提取tag号去索引
                        bom.append([fit[0], fit[0] + '_' + fit[7], fit[5], fit[9], int(fit[4]), 'EA', fit[10], fit[11]])
                    else:
                        bom.append([fit[0], fit[0] + '_' + fit[7], fit[5], fit[2], int(fit[4]), 'EA', fit[10], fit[11]])

        write_to_excel('bom.xlsx',bom)
        
        #iMES_BOM
        line_rev = 1
        spool_rev = 1
        imes_bom = [['workorder_no','line_no','line_rev','spool_no','spool_rev','code','part_no','phrase','group','size','quantity','unit','desc']]
        
        for m in module_name:
            f_material_list_for_imes = module_path + m + '\\' +  sub_folder_name + raw_material_list_for_imes            
            fittings = file_to_list(f_material_list_for_imes,raw_material_list_for_imes_index)
            
            for fitting in fittings:
                if not('---' in fitting[0] ):
                    line_no,spool_no,code,group,size,quantity,part_no,pharse,desc = fitting
                    size = size.strip('"')
                    if group == 'Pipe' :
                        unit = 'M'
                        quantity = float(quantity) / 1000.0
                    else:
                        unit = 'EA'
                        quantity = 1
                    tmp = [workorder_no,line_no,line_rev,line_no + '_' + spool_no,spool_rev,code,part_no,pharse,group,size,quantity,unit,desc]
                    imes_bom.append(tmp)

        write_to_excel('imes_bom.xlsx',imes_bom)

        #iMES_Weld
        imes_weld = [['workorder_no','line_no','line_rev','spool_no','spool_rev','weld_no','size','part_no1','part_no2','conn_type','fab_type']]
        
        for m in module_name:
            f_welding_list_for_imes = module_path + m + '\\' +  sub_folder_name + raw_welding_list_for_imes

            fittings = file_to_list(f_welding_list_for_imes,raw_welding_list_for_imes_index)
            
            for fitting in fittings:
                if not('---' in fitting[0] ):
                    line_no, weld_no, size, conn_type, fab_type, pipe_class, rev, spool_no,part_no = fitting
                    size = fraction_to_decimal(size.strip('"'))
                    part_no1,part_no2 = part_no.split('-')
                    tmp = [workorder_no,line_no,line_rev,line_no + '_' + spool_no,spool_rev,weld_no,size,part_no1,part_no2,conn_type,fab_type]
                    imes_weld.append(tmp)

        write_to_excel('imes_weld.xlsx',imes_weld)

        print 'Done!'

























