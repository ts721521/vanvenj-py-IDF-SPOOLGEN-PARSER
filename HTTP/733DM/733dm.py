# -*- coding:utf8 -*-

import re
import base64
import requests
import jsbeautifier
from bs4 import BeautifulSoup

def get_content(main_url):
    r = requests.get(main_url)
    soup = BeautifulSoup(r.content, "lxml")
    url_root = 'http://www.733dm.net'
    with open('list.txt','w') as f:
        for li in soup.find('div',id=re.compile('^play_')).findAll('li'):
            f.write(url_root + li.find('a')['href'] + '\n')
        
def get_topic(topic_url):
    r = requests.get(topic_url)
    packed = re.findall('(?<=packed=").*(?=")',r.content)[0]
    viewname = re.findall('(?<=viewname = ").*(?=")',r.content)[0].replace(' ','')
    jspacker = base64.b64decode(packed)
    image_paths = jsbeautifier.beautify(jspacker)
    url_root="http://733dm.zgkouqiang.cn/"
    image_urls = [(lambda x:url_root + x)(x)for x in re.findall('(?<=").*(?=")',image_paths)]
    for i,image_url in enumerate(image_urls):
        save_image(image_url,viewname + '_' + str(i+1)+ '_' + image_url.split('/')[-1])  

def save_image(img_url,img_name):
    r = requests.get(img_url)
    with open('.\\downloads\\'+img_name,'wb') as f:
        f.write(r.content)

if __name__ == '__main__':
    main_url='http://www.733dm.net/mh/13055/'
    get_content(main_url)
    with open('list.txt','r') as f:
        for line in f:
            topic_url = line.replace('\n','')
            print 'Start Downloading' + topic_url
            with open('download.txt','a') as log:
                log.write(topic_url + '\n')
            get_topic(topic_url)
            print topic_url + ' finished!'
            with open('download.txt','a') as log:
                log.write(topic_url + ' finished\n')
        




