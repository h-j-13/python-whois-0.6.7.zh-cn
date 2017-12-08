# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from future import standard_library
standard_library.install_aliases()
from builtins import *
import re
import sys
import os
import subprocess
import socket
from .parser import WhoisEntry  # WHOIS解析模板
from .whois import NICClient    # WHOIS服务器通信客户端


# 核心函数
def whois(url, command=False):  
    # clean domain to expose netloc
    ip_match = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", url)
    # 如果输入了IP
    if ip_match:
        domain = url
        try:    # 提取ip之后反向解析出主机名
            result = socket.gethostbyaddr(url)
        except socket.herror as e:
            pass
        else:
            domain = result[0]
    # 如果输入了域名
    else:   # 对域名进行处理 FQDN -> Domain        
            # eg: https://www.baidu.com/p/12131 -> baidu.com
        domain = extract_domain(url)
    # 获取域名WHOIS方式供两种
    # 一:基于linux的原生whois命令
    if command:
        # try native whois command
        r = subprocess.Popen(['whois', domain], stdout=subprocess.PIPE)
        text = r.stdout.read()
    # 二:基于自己封装的socket链接通信
    else:
        # try builtin client
        nic_client = NICClient()
        text = nic_client.whois_lookup(None, domain.encode('idna'), 0)
    
    return WhoisEntry.load(domain, text)


suffixes = None
def extract_domain(url):
    """Extract the domain from the given URL

    >>> print(extract_domain('http://www.google.com.au/tos.html'))
    google.com.au
    >>> print(extract_domain('abc.def.com'))
    def.com
    >>> print(extract_domain(u'www.公司.hk'))
    公司.hk
    >>> print(extract_domain('chambagri.fr'))
    chambagri.fr
    >>> print(extract_domain('www.webscraping.com'))
    webscraping.com
    >>> print(extract_domain('198.252.206.140'))
    stackoverflow.com
    >>> print(extract_domain('102.112.2O7.net'))
    2o7.net
    >>> print(extract_domain('globoesporte.globo.com'))
    globo.com
    >>> print(extract_domain('1-0-1-1-1-0-1-1-1-1-1-1-1-.0-0-0-0-0-0-0-0-0-0-0-0-0-10-0-0-0-0-0-0-0-0-0-0-0-0-0.info'))
    0-0-0-0-0-0-0-0-0-0-0-0-0-10-0-0-0-0-0-0-0-0-0-0-0-0-0.info
    """
    # todo
    # ??? 着咯不是和上面判断重复了吗???
    if re.match(r'\d+\.\d+\.\d+\.\d+', url):
        # this is an IP address
        return socket.gethostbyaddr(url)[0]
    
    # 基于已知TLD进行域名解析
    # load known TLD suffixes
    global suffixes
    if not suffixes:    # 初次读取 publicsuffix 的公开一级/二级 TLD 进行域名解析
        # downloaded from https://publicsuffix.org/list/public_suffix_list.dat
        tlds_path = os.path.join(os.getcwd(), os.path.dirname(__file__), 'data', 'public_suffix_list.dat')
        with open(tlds_path, encoding='utf-8') as tlds_fp:
            suffixes = set(line.encode('utf-8') for line in tlds_fp.read().splitlines() if line and not line.startswith('//'))
    # 对编码进行格式转换
    if not isinstance(url, str):
        url = url.decode('utf-8')
    url = re.sub('^.*://', '', url)
    url = url.split('/')[0].lower()

    # find the longest suffix match
    # 通过在域名中寻找已知最长的后缀来提取域名的正确格式

    # todo ? 找到不到怎么办?
    domain = b''
    for section in reversed(url.split('.')):
        if domain:
            domain = b'.' + domain
        domain = section.encode('utf-8') + domain
        if domain not in suffixes:
            break
    return domain.decode('utf-8')


if __name__ == '__main__':
    try:
        url = sys.argv[1]
    except IndexError:
        print('Usage: %s url' % sys.argv[0])
    else:
        print(whois(url))
