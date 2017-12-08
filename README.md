python-whois-0.6.7 
======================
源码解析,中文


## 简介
一个方便易用的WHOIS查询库

### 说明

- 适用于Python 2＆3
- 能够提取所有流行顶级域名（com，org，net，...）的数据
- 将WHOIS服务器返回的数据自动进行解析,提取关键项
- 直接查询WHOIS服务器，而不是去访问第三方网站或者其他数据源。

### 使用
```python
    >>> import whois
    >>> w = whois.whois('webscraping.com')
    >>> w.expiration_date  # dates converted to datetime object
    datetime.datetime(2013, 6, 26, 0, 0)
    >>> w.text  # the content downloaded from whois server
    u'\nWhois Server Version 2.0\n\nDomain names in the .com and .net 
    ...'

    >>> print w  # print values of all found attributes
    creation_date: 2004-06-26 00:00:00
    domain_name: [u'WEBSCRAPING.COM', u'WEBSCRAPING.COM']
    emails: [u'WEBSCRAPING.COM@domainsbyproxy.com', u'WEBSCRAPING.COM@domainsbyproxy.com']
    expiration_date: 2013-06-26 00:00:00
    ...
```

### 安装

```bash
$ pip install python-whois
```

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
└─whois                             \\  WHOIS 库
    │  parser.py                    \\  WHOIS 解析模板
    │  time_zones.py                \\  时区数据 更好的处理时间属性 
    │  whois.py                     \\  WHOIS链接客户端,请求构造,域名处理及解析,WHOIS服务器选择
    │  __init__.py                  \\  WHOIS 主函数入口
    │   
    └─data                          \\  数据目录
          └─ public_suffix_list.dat \\  https://publicsuffix.org/list/ 上的

额外目录:TEMP
-------------------------------------------
里面存放了 [WHOIS 0.7](https://pypi.python.org/pypi/whois/) 的WHOIS信息解析正则表达式集
WHOIS 0.7 是一个 2012年的 基于Linux的WHOIS命令的域名WHOIS查询库
源码较少,无特别需要关注的地方
```

## 源码解析
入口:``__init__.py``` --- whois函数
其他所有函数均在代码中在代码中标注了添加的中文注释

## 特点
### 获取WHOIS流程
输入FQDN -> 进行FQDN解析 -> 获取域名 -> 选择对应的WHOIS服务器 -> 构造合适的请求 -> 解析返回数据,找出详细信息所在的WHOIS服务器 -> 构造请求 -> 获取WHOIS信息

### 域名解析流程
这里没有使用tldextract库或者其他基于字符串解析域名的方式,      
而是从 https://publicsuffix.org/list/public_suffix_list.dat 里获取当前所有的一级和二级域名后缀      
通过在需要解析的域名中匹配最长的后缀来找出域名所在的位置,并提取
 
### 获取WHOIS服务器地址过程
这里还是缺少了部分依据,WHOIS服务器总体数量较少      
基本一次WHOIS获取过程总要请求两次WHOIS服务器,相当于降低了一半的效率     
但不使用数据库的前提下,此方式倒是比较简洁

### 解析WHOIS数据,提取关键信息
这里采用了基类+继承的方式       
构建了多个WHOIS解析类,针对解析WHOIS返回的数据.       
这部分正则表达式比较有参考价值

## 最后
H-J-13(@`13)                                         
z.g.13@163.com/h.j.13.new@gmail.com                 
Harbin Institute of Technology at Weihai     

[`13 Blog](http://houjie13.com/)        
[`13的博客](http://www.jianshu.com/u/75156f101757)	