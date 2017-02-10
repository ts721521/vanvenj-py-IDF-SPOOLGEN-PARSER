# 关于此脚本
森松信息平台添加物料编码需要在网页上点击按钮执行。
对于大量的编码添加较为麻烦。
利用python的HTTP POST功能可以较为方便的添加大量的编码。


# python库要求
- 需要requests库,处理http协议
- 需要bs库，python版的jQuery，快速选择页面元素
- 用阿里云镜像批量安装
```
pip install --trusted-host=mirrors.aliyun.com --index-url=http://mirrors.aliyun.com/pypi/simple/ -r requirement.txt
```

- requirement.txt
  - beautifulsoup4==4.4.1
  - requests==2.8.1


# 其他
- 需要借助fidder抓取一次浏览器post的数据，否则有些字段不知道填写什么。


