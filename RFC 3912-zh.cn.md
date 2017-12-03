```
Network Working Group                                          L. Daigle
Request for Comments: 3912                                VeriSign, Inc.
Obsoletes: 954, 812                                       September 2004
Category: Standards Track
```

#                      WHOIS 协议规范

### 本备忘录状态

   This document specifies an Internet standards track protocol for the     
   Internet community, and requests discussion and suggestions for      
   improvements.  Please refer to the current edition of the "Internet      
   Official Protocol Standards" (STD 1) for the standardization state       
   and status of this protocol.  Distribution of this memo is unlimited.        

### 版权声明

   Copyright (C) The Internet Society (2004).       

### 摘要

  本文档更新了 WHOIS协议 的规范,从而废除RFC 954.     
  该更新旨在删除来自RFC 954的材料与线上无关协议，     
  不再适用于当今的互联网。        
  这个文档不会尝试更改或更新协议本身，或者
  记录自RFC 954发布以来已经存在的协议的其他用途。

### 1.  介绍

  WHOIS一个是基于TCP的面向事务的查询/响应协议       
  其广泛被应用于向互联网用户提供信息查询服务       
  虽然最初用来提供“白页”服务和有关注册域名的信息      
  但是当前的部署涵盖了内容了更广泛的信息服务。   
  该协议以可读格式传送其内容。本文件更新了        
  规范WHOIS协议，从而废除RFC 954 [1]。  

  由于历史原因，WHOIS缺乏很多协议设计属性,         
  例如国际化和强壮安全性，这可以从最近设计的IETF协议中预料到。        
  本文不会尝试纠正任何这些缺点。相反，这份备忘录     
  如是记录了WHOIS协议的情况。在某些地方       
  本文确实记录了一些WHOIS协议的众所周知的缺点。       
  有关于协议可能带来的新的功能与更新所带来的缺陷的相关讨论,       
  正在单独的IETF活动中处理（CRISP 工作小组）。     


### 2.  协议规范

  WHOIS服务器在TCP端口43上侦听来自WHOIS客户端的请求。      
  WHOIS客户端向WHOIS服务器发送文本请求,然后      
  WHOIS服务器以文本内容回应。所有的请求都是     
  以ASCII码<CR>接ASCII码<LF>结尾。回应可能       
  包含多行文本，所以存在ASCII码<CR>或      
  ASCII码<LF>字符不表示响应结束。该响应输出完成后，     
  WHOIS服务器立即关闭与WHOIS客户端的连接。       
  关闭的TCP连接是对客户端的指示回应已收到。      

### 3.  协议样例

  如果有人向位于whois.nic.mil的WHOIS服务器请求     
  有关"Smith"的信息,在网络上传送的数据包将会像是这样:      

    ```
    WHOIS客户端                位于 whois.nic.mil 的WHOIS服务器 

    打开 TCP      ---- (SYN) ------------------------------>
                <---- (SYN+ACK) -------------------------
    发送查询    ---- "Smith<CR><LF>" -------------------->
    获得响应    <---- "有关于 Smith 的信息<CR><LF>" ---------
                <---- "更多有关于 Smith 的信息<CR><LF>" ----
    关闭          <---- (FIN) ------------------------------
                ----- (FIN) ----------------------------->
    ```

### 4.  国际化

  WHOIS协议尚未国际化。 WHOIS     
  协议没有指示正在使用的字符集的机制。      
  最初，主要使用的文本编码是US-ASCII。在     
  实际中，一些WHOIS服务器，尤其是美国境外的服务器，     
  可能会使用其他字符集来解析请求或发出回应。      
  无法预测或表示的文本编码了对此WHOIS协议的     
  的互通性(当然,也包括可用性)有着不利的影响.     


### 5.  安全性考虑

  WHOIS协议没有强有力的安全措施。WHOIS协议       
  缺乏有关访问控制，完整性和机密性的机制。        
  因此，基于WHOIS的服务只能用于非敏感的信息     
  并准备让所有人都可以访问。      
  此项安全机制的缺失意味着在本协议编写时
  通常可能不会被IETF所接受 


## 6. 致谢
  
  Ran Atkinson created an earlier version of this document.  Ken          
  Harrenstien, Mary Stahl, and Elizabeth Feinler were the authors of          
  the original Draft Standard for WHOIS.       

### 7.  参考文献

7.1.  Normative References

> [1]  Harrenstien, K., Stahl, M., and E. Feinler, "NICNAME/WHOIS", RFC
954, October 1985.

### 作者地址

   Leslie Daigle    
   VeriSign, Inc.   
   21355 Ridgetop Circle    
   Dulles, VA  20166    
   US   

   EMail: leslie@verisignlabs.com; leslie@thinkingcat.com   
   
### 完整版权声明

   Copyright (C) The Internet Society (2004).       

   This document is subject to the rights, licenses and restrictions        
   contained in BCP 78, and at www.rfc-editor.org, and except as set        
   forth therein, the authors retain all their rights.      

   This document and the information contained herein are provided on an        
   "AS IS" basis and THE CONTRIBUTOR, THE ORGANIZATION HE/S HE      
   REPRESENTS OR IS SPONSORED BY (IF ANY), THE INTERNET SOCIETY AND THE     
   INTERNET ENGINEERING TASK FORCE DISCLAIM ALL WARRANTIES, EXPRESS OR      
   IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTY THAT THE USE OF       
   THE INFORMATION HEREIN WILL NOT INFRINGE ANY RIGHTS OR ANY IMPLIED       
   WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.       

### 知识产权

   The IETF takes no position regarding the validity or scope of any        
   Intellectual Property Rights or other rights that might be claimed to        
   pertain to the implementation or use of the technology described in      
   this document or the extent to which any license under such rights       
   might or might not be available; nor does it represent that it has       
   made any independent effort to identify any such rights.  Information        
   on the ISOC's procedures with respect to rights in ISOC Documents can        
   be found in BCP 78 and BCP 79.       

   Copies of IPR disclosures made to the IETF Secretariat and any       
   assurances of licenses to be made available, or the result of an     
   attempt made to obtain a general license or permission for the use of        
   such proprietary rights by implementers or users of this     
   specification can be obtained from the IETF on-line IPR repository at        
   http://www.ietf.org/ipr.     

   The IETF invites any interested party to bring to its attention any      
   copyrights, patents or patent applications, or other proprietary     
   rights that may cover technology that may be required to implement       
   this standard.  Please address the information to the IETF at ietf-      
   ipr@ietf.org.        

### 致谢

   Funding for the RFC Editor function is currently provided by the     
   Internet Society.        


