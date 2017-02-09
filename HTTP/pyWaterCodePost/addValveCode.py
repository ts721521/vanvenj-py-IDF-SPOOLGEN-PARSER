# -*- coding:utf8 -*-

from requests import session 
from bs4 import BeautifulSoup

#通过登录与服务器建立连接
loginUrl = 'http://199.234.20.170:8032/login.aspx'
s = session()
r = s.get(loginUrl)
bs = BeautifulSoup(r.text,"lxml")
__VIEWSTATE = bs.select('#__VIEWSTATE')[0].get('value')
__EVENTVALIDATION = bs.select('#__EVENTVALIDATION')[0].get('value')
__VIEWSTATEGENERATOR = bs.select('#__VIEWSTATEGENERATOR')[0].get('value')
loginData = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__LASTFOCUS': '',
    '__VIEWSTATE':__VIEWSTATE,
    '__VIEWSTATEGENERATOR':__VIEWSTATEGENERATOR,
    '__EVENTVALIDATION':__EVENTVALIDATION,
    'txtUsername':'6016',
    'txtPass':'1',
    'btnLogin':'登 录',
    'rbl_language':'cn',
    }
s.post(loginUrl, loginData)

#读取需要创建的流水码清单
f = open('valveList.txt','r')
data = f.readlines()
f.close()

#遍历流水码，执行post，提交数据
for i in range(data.__len__()):
    #windows下的文本默认是cp936格式，需要解码成Unicode
    desc = data[i].split('\t')[1].decode('cp936')
    remark = data[i].split('\t')[2].decode('cp936')
    
    print i+1,'/',data.__len__()
    

    operateUrl = 'http://199.234.20.170:8032/DataSelfDefine/PostInfo.aspx'

    #注意，以下数据需要利用fidder抓取一次浏览器行为，不可乱填
    operateData = {
        'meunid':'126',
        'strPKValue':'0',
        'action':'add',
        'project_id':'2339',
        'workorder_no':'JMH16-M-80335',
        'major_category_id':'22',
        'classification_info_id':'989',
        'material_desc':desc,
        'remark':remark,
        'alternative_code':'',
        'phd_item_group':'',
        'phd_item_type':'',
        'weight':''
        }

    #森松平台有个bug，post之后没有返回，所以要处理意外
    try:
        r = s.post(operateUrl,operateData)
    except:
        pass
