# -*- coding: utf-8 -*-

# python WHOIS客户端
"""
Whois client for python

transliteration of:
http://www.opensource.apple.com/source/adv_cmds/adv_cmds-138.1/whois/whois.c

Copyright (c) 2010 Chris Wolf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
import re
import sys
import socket
import optparse


class NICClient(object):
    
    # WHOIS 服务器列表
    ABUSEHOST = "whois.abuse.net"
    NICHOST = "whois.crsnic.net"
    INICHOST = "whois.networksolutions.com"
    DNICHOST = "whois.nic.mil"
    GNICHOST = "whois.nic.gov"
    ANICHOST = "whois.arin.net"
    LNICHOST = "whois.lacnic.net"
    RNICHOST = "whois.ripe.net"
    PNICHOST = "whois.apnic.net"
    MNICHOST = "whois.ra.net"
    QNICHOST_TAIL = ".whois-servers.net"
    SNICHOST = "whois.6bone.net"
    BNICHOST = "whois.registro.br"
    NORIDHOST = "whois.norid.no"
    IANAHOST = "whois.iana.org"
    PANDIHOST = "whois.pandi.or.id"
    DENICHOST = "de.whois-servers.net"
    AI_HOST = "whois.ai"
    DEFAULT_PORT = "nicname"

    WHOIS_RECURSE = 0x01
    WHOIS_QUICK = 0x02

    ip_whois = [LNICHOST, RNICHOST, PNICHOST, BNICHOST, PANDIHOST]

    def __init__(self):
        self.use_qnichost = False

    def findwhois_server(self, buf, hostname, query):
        # 从返回数据里查询域名具体WHOIS信息所在的WHOIS服务器
        """Search the initial TLD lookup results for the regional-specifc
        whois server for getting contact details.
        """
        # 先去一级WHOIS服务器上查询此域名对应的WHOIS服务器地址 并返回
        nhost = None
        match = re.compile('Domain Name: ' + query + '\s*.*?Whois Server: (.*?)\s', flags=re.IGNORECASE|re.DOTALL).search(buf)
        if match:
            nhost = match.groups()[0]
            # if the whois address is domain.tld/something then
            # s.connect((hostname, 43)) does not work
            if nhost.count('/') > 0:
                nhost = None    # 假如WHOIS服务器有/ 则抛弃其
        #　也就是所　"whois.arin.net"　的返回格式于其他WHOIS并不相同　且此WHOIS服务有且仅有　LNICHOST, RNICHOST, PNICHOST, BNICHOST, PANDIHOST　WHOIS服务器
        elif hostname == NICClient.ANICHOST:    # 找不的话 如果查询的WHOIS服务器为  "whois.arin.net"
            for nichost in NICClient.ip_whois:  # 则从 LNICHOST, RNICHOST, PNICHOST, BNICHOST, PANDIHOST 找到需要查询的WHOIS服务器
                if buf.find(nichost) != -1: # 
                    nhost = nichost
                    break
        return nhost


    def whois(self, query, hostname, flags, many_results=False):
        """Perform initial lookup with TLD whois server
        then, if the quick flag is false, search that result
        for the region-specifc whois server and do a lookup
        there for contact details
        """
        response = b''
        try: # socket通信 ipv4 超时10s 连结43端口
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((hostname, 43))

            try:    # 转为UTF8编码
                query = query.decode('utf-8')
            except UnicodeEncodeError:
                pass  # Already Unicode (python2's error)
            except AttributeError:
                pass  # Already Unicode (python3's error)

            # 根据需要查询的WHOIS服务器优化查询格式
            if hostname == NICClient.DENICHOST: # de whois服务器
                query_bytes = "-T dn,ace -C UTF-8 " + query # dewhois服务器的 特殊的查询请求
            elif hostname.endswith(NICClient.QNICHOST_TAIL) and many_results:   # 如果WHOIS服务器
                query_bytes = '=' + query                                       # .whois-servers.net 结尾            
            else:                                                               # 则加上在查询前面加  = 
                query_bytes = query
            # 发送查询请求    
            s.send(bytes(query_bytes,'utf-8') + b"\r\n")    
            # 接收数据 
            # recv returns bytes
            while True:
                d = s.recv(4096)
                response += d
                if not d:
                    break
            # 接收数据之后关闭socket 捕获异常后输出
            s.close()
        except socket.error as socketerror:         # ??? 这个try-except包的范围稍微有点大了..
            print('Socket Error:', socketerror)     # 其次,为什么是建立连接之后整理查询数据呢 而不是先整理好 然后建立连接 发送查询数据

        nhost = None
        response = response.decode('utf-8', 'replace')
        if 'with "=xxx"' in response:
            return self.whois(query, hostname, flags, True)
        if flags & NICClient.WHOIS_RECURSE and nhost is None:
            nhost = self.findwhois_server(response, hostname, query)
        if nhost is not None:
            response += self.whois(query, nhost, 0)
        return response

    def choose_server(self, domain):
        """Choose initial lookup NIC host"""

        # 处理编码问题
        try:
            domain = domain.encode('idna').decode('utf-8')
        except TypeError:
            domain = domain.decode('utf-8').encode('idna').decode('utf-8')
        except AttributeError:
            domain = domain.decode('utf-8').encode('idna').decode('utf-8')


        # 域名以 -NORID 结尾 -> whois.norid.no
        if domain.endswith("-NORID"):
            return NICClient.NORIDHOST
        # 域名以 id 结尾 -> "whois.pandi.or.id
        if domain.endswith("id"):
            return NICClient.PANDIHOST
        # 找出tld
        domain = domain.split('.')
        if len(domain) < 2:
            return None
        # 找出顶级域
        tld = domain[-1]
        if tld[0].isdigit():    # 顶级域第一个字母是数字 -> whois.arin.net
            return NICClient.ANICHOST
        # 顶级域ai ->  whois.ai
        elif tld == 'ai':
            return NICClient.AI_HOST
        
        # 顶级域为其他的时候  -> 顶级域 + .whois-servers.net
        else:       ### ??? 有没有理论依据啊
            return tld + NICClient.QNICHOST_TAIL

    def whois_lookup(self, options, query_arg, flags):
        # WHOIS 查询主函数
        """Main entry point: Perform initial lookup on TLD whois server,
        or other server to get region-specific whois server, then if quick
        flag is false, perform a second lookup on the region-specific
        server for contact records"""
        nichost = None
        # whoud happen when this function is called by other than main
        if options is None:
            options = {}

        if ('whoishost' not in options or options['whoishost'] is None) \
                and ('country' not in options or options['country'] is None):
            self.use_qnichost = True
            options['whoishost'] = NICClient.NICHOST
            if not (flags & NICClient.WHOIS_QUICK):
                flags |= NICClient.WHOIS_RECURSE

        if 'country' in options and options['country'] is not None:
            result = self.whois(
                query_arg,
                options['country'] + NICClient.QNICHOST_TAIL,
                flags
            )
        elif self.use_qnichost:
            nichost = self.choose_server(query_arg)
            if nichost is not None:
                result = self.whois(query_arg, nichost, flags)
            else:
                result = ''
        else:
            result = self.whois(query_arg, options['whoishost'], flags)
        return result


def parse_command_line(argv):
    """Options handling mostly follows the UNIX whois(1) man page, except
    long-form options can also be used.
    """
    flags = 0

    usage = "usage: %prog [options] name"

    parser = optparse.OptionParser(add_help_option=False, usage=usage)
    parser.add_option("-a", "--arin", action="store_const",
                      const=NICClient.ANICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.ANICHOST)
    parser.add_option("-A", "--apnic", action="store_const",
                      const=NICClient.PNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.PNICHOST)
    parser.add_option("-b", "--abuse", action="store_const",
                      const=NICClient.ABUSEHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.ABUSEHOST)
    parser.add_option("-c", "--country", action="store",
                      type="string", dest="country",
                      help="Lookup using country-specific NIC")
    parser.add_option("-d", "--mil", action="store_const",
                      const=NICClient.DNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.DNICHOST)
    parser.add_option("-g", "--gov", action="store_const",
                      const=NICClient.GNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.GNICHOST)
    parser.add_option("-h", "--host", action="store",
                      type="string", dest="whoishost",
                      help="Lookup using specified whois host")
    parser.add_option("-i", "--nws", action="store_const",
                      const=NICClient.INICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.INICHOST)
    parser.add_option("-I", "--iana", action="store_const",
                      const=NICClient.IANAHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.IANAHOST)
    parser.add_option("-l", "--lcanic", action="store_const",
                      const=NICClient.LNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.LNICHOST)
    parser.add_option("-m", "--ra", action="store_const",
                      const=NICClient.MNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.MNICHOST)
    parser.add_option("-p", "--port", action="store",
                      type="int", dest="port",
                      help="Lookup using specified tcp port")
    parser.add_option("-Q", "--quick", action="store_true",
                      dest="b_quicklookup",
                      help="Perform quick lookup")
    parser.add_option("-r", "--ripe", action="store_const",
                      const=NICClient.RNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.RNICHOST)
    parser.add_option("-R", "--ru", action="store_const",
                      const="ru", dest="country",
                      help="Lookup Russian NIC")
    parser.add_option("-6", "--6bone", action="store_const",
                      const=NICClient.SNICHOST, dest="whoishost",
                      help="Lookup using host " + NICClient.SNICHOST)
    parser.add_option("-n", "--ina", action="store_const",
                          const=NICClient.PANDIHOST, dest="whoishost",
                          help="Lookup using host " + NICClient.PANDIHOST)
    parser.add_option("-?", "--help", action="help")

    return parser.parse_args(argv)


if __name__ == "__main__":
    flags = 0
    nic_client = NICClient()
    options, args = parse_command_line(sys.argv)
    if options.b_quicklookup:
        flags = flags | NICClient.WHOIS_QUICK
    print(nic_client.whois_lookup(options.__dict__, args[1], flags))
