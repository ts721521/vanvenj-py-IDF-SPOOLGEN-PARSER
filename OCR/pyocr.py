# -*- coding: utf-8 -*-

#使用requests访问ocr.space,获取图像识别结果
def ocr_space_file(filename, overlay=True, api_key='helloworld', language='eng'):
    import requests
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()

#使用正则表达式提取返回文件中的字符信息
def get_data_with_re(json_file):
    import re
    with open(json_file,'r') as f:
        lines = re.findall(r'{"WordText".+?}',f.read())
    return lines

#输出频率分布柱状图
def plotHistogram(x,maxX):
    plt.hist(x,100)
    plt.xlabel('Position')
    plt.xlim(0.0,maxX)
    plt.ylabel('Frequency')
    plt.title('Pos Frequency')
    plt.show()


if __name__ == '__main__':
    ##obtain json file form api
    #test_file = ocr_space_file(filename='sample.png')
    #with open('sample.json','w') as f:
    #    f.write(test_file)
    import json 
    import matplotlib.pyplot as plt
    from PIL import Image
    img = Image.open('sample.png')

    #parse json data  
    words = get_data_with_re('sample.json')

    print map((lambda w : [w['Left'],w['Top'] + w['Height'],w['WordText'],w['Height'],w['Width'], (w['Top'] + w['Height']) / 15 ]),words)
    
### 获取Y坐标    
##    wordDict = []
##    for word in words:
##        w = json.loads(word)
##        wordDict.append([w['Left'],w['Top'] + w['Height'],w['WordText'],w['Height'],w['Width'], (w['Top'] + w['Height']) / 15 ])
##

# 绘制柱状图
##    xPos = []
##    for _ in wordDict:
##        xPos.append(_[0])
##
##    plotHistogram(xPos,700)


    
# 按矫正Y坐标排序
##    for i in sorted(wordDict,key = lambda x: x[5]):
##        print i
    

# 在图片中显示识别信息
##    plt.figure('ocr')
##    plt.imshow(img)
##    
##    for word in words:
##        w = json.loads(word)
##        plt.text(w['Left'],w['Top'] + w['Height'],w['WordText'],fontsize=w['Height'],color='red')
##
##    plt.show()
