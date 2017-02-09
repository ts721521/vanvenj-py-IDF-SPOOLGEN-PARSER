# 关于 pyAddSignature
对文件夹中的PDF图纸文件批量添加电子签名

# 使用须知
- 需要安装python2.7
- 需要安装PyPDF2包，使用阿里云镜像安装，速度比较快
```
pip install --trusted-host=mirrors.aliyun.com --index-url=http://mirrors.aliyun.com/pypi/simple/ PyPDF2
```

# 如何使用
1. 下载pyAddSignature.py
2. 执行python AddSignature.py 初始化文件夹
3. 将需要添加电子签名的pdf放到input_files文件夹下
4. 用AutoCAD制作电子签名，并且打印对应尺寸(A3)的PDF，放到程序同级目录下
5. 修改AddSignature.py文件中签名文件和签名偏移量，在主函数下面。
6. 执行python AddSignature.py 查看结果，如果位置不对，调整偏移量。

