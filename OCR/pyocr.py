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

def get_data_with_re(json_file):
    '''
    使用正则表达式提取返回文件中的字符信息
    返回格式如下：
    [
        [Left,Top,WordText,Height,Width],
        [Left,Top,WordText,Height,Width],
        ...
    ]
    '''
    import re
    import json
    words = []
    with open(json_file,'r') as f:
        lines = re.findall(r'{"WordText".+?}',f.read())
    for line in lines:
        word = json.loads(line)
        words.append([word['Left'],word['Top'],word['WordText'],word['Height'],word['Width']])
    return words

def plotHistogram(x):
    '''
    输出频率分布柱状图
    '''
    import numpy as np
    bins = np.arange(min(x),max(x),1)
    data =  plt.hist(x,bins=bins)
    plt.xlabel('Value')
    plt.xlim(min(x)-10,max(x)+10)
    plt.ylabel('Frequency')
    plt.title('Frequency Count')
    plt.show()
    return data

if __name__ == '__main__':
    ##obtain json file form api
    #test_file = ocr_space_file(filename='sample.png')
    #with open('sample.json','w') as f:
    #    f.write(test_file)

    import json 
    import matplotlib.pyplot as plt
    from PIL import Image
    img = Image.open('sample.png')

    #获取解析后的json data  
    words = get_data_with_re('sample.json')

    #获取x，y，Height的数据集
    xPositions = [(lambda x:x[0])(x) for x in words]
    yPositions = [(lambda x:x[1])(x) for x in words]
    Heights = [(lambda x:x[3])(x) for x in words]

    import collections
    c = collections.Counter(yPositions)
    yPosCount = zip(c.keys(),c.values())
    print sorted(yPosCount,key = lambda x:x[0])

    #绘制柱状图
    plotHistogram(yPositions)



    
# 按矫正Y坐标排序
##    for i in sorted(wordDict,key = lambda x: x[5]):
##        print i
    

    #在图片中显示识别信息
    #plt.figure('ocr')
    #plt.imshow(img)
    #
    #for w in words:
    #    plt.text(w[0],round((w[1] + w[3]) / 10.0 )* 10 ,w[2],fontsize=10,color='red')
    #plt.show()
