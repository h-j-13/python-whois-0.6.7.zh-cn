python-whois-0.6.7 
======================
阅读源码注释


## 简介

## 库文件结构及说明

### 官方说明    

[python-whois-0.6.7](https://pypi.python.org/pypi/python-whois)


| File  | Type  | Py Version    | Uploaded on   | Size  |
| :---- | :---- | :------------ | :------------ | :---- |
|python-whois-0.6.7.tar.gz (md5)|Source| |2017-12-01|79KB|


- Author: Richard Penman  
- Home Page: https://bitbucket.org/richardpenman/pywhois  
- Keywords: whois,python  
- License: MIT    
- Categories  
    - Environment :: Web Environment  
    - Intended Audience :: Developers 
    - License :: OSI Approved :: MIT License  
    - Operating System :: OS Independent  
    - Programming Language :: Python  
    - Topic :: Internet :: WWW/HTTP   
- Package Index Owner: Richard.Penman  
- DOAP record: python-whois-0.6.7.xml 

### 源码目录结构说明

```
python-whois-0.6.7      
│  MANIFEST.in                      \\  编译说明文件
│  PKG-INFO                         \\  包信息说明
│  README.rst                       \\  说明&文档
│  setup.cfg                        \\  安装参数
│  setup.py                         \\  安装脚本
│ 
├─python_whois.egg-info             \\  包详细信息
│      dependency_links.txt         \\  依赖链接
│      not-zip-safe                 \\  zip不安全
│      PKG-INFO                     \\  包信息
│      requires.txt                 \\  需求 python-dateutil 第三方包用于更好的解析提取日期
│      SOURCES.txt                  \\  源码目录说明
│      top_level.txt                \\  顶级目录说明
│
├─test                              \\  单元测试
│      test_main.py                 \\  域名提取测试
│      test_nicclient.py            \\  WHOIS服务器地址选择测试
│      test_parser.py               \\  域名WHOIS数据解析测试
│      test_query.py                \\  多种域名类型及编码测试
│       
└─whois                             \\
    │  parser.py                    \\
    │  time_zones.py                \\
    │  whois.py                     \\
    │  __init__.py                  \\
    │   
    └─data                          \\
          └─ public_suffix_list.dat \\  
```

## WHOIS理论及获取理论说明

## 源码解析

## 最后

