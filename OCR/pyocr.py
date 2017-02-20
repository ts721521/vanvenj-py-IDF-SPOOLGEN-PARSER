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
    

if __name__ == '__main__':
    #test_file = ocr_space_file(filename='sample.png')
    #with open('sample.json','w') as f:
    #    f.write(test_file)
    import json 
    import matplotlib.pyplot as plt
    from PIL import Image
    img = Image.open('sample.png')
    words = get_data_with_re('sample.json')
    plt.figure('ocr')
    plt.imshow(img)

    for word in words:
        w = json.loads(word)
        plt.text(w['Left'],w['Top'] + w['Height'],w['WordText'],fontsize=w['Height'],color='red')

    plt.show()
