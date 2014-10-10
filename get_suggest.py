#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Hito www.hitoy.org
import urllib2,sys,time,os
from xml.etree import ElementTree

class keywords():
    def __init__(self):
        self.user_agent="Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36"
        self.Accept="text/html application/xhtml+xml,application/xml */*"
        self.Connection="close"
    def get_search_suggest(self,key,filename):
        try:
            key=urllib2.quote(key)
            req=urllib2.Request("http://search.yahoo.com/sugg/gossip/gossip-us-ura/?command=%s"%key)
            req.add_header("Accept",self.Accept)
            req.add_header("Connection",self.Connection)
            req.add_header("Referer","http://search.yahoo.com")
            req.add_header("user_agent",self.user_agent)
            res=urllib2.urlopen(req)
            html=res.read()
            words=self.__read_xml(html)
            self.__save_to_file(words,filename)
            notek=urllib2.unquote(key)
            print u"%s 扩展成功"%(notek)
        except:
            print "Some thing error!"
    def __read_xml(self,text):
        words=""
        root=ElementTree.fromstring(text)
        node_findall = root.findall("s")
        for i in node_findall:
            words=words+i.attrib["k"]+"\n"
        return words
    def __save_to_file(self,content,filename):
        suggestfile=open(filename,"a")
        suggestfile.write(content)
        suggestfile.close()



print u"========================================"
print u"==关键词生成程序 by Hito www.hitoy.org=="
print u"========================================"
if not(sys.argv[1:]):
    print ""
    print u"关键词生成程序以命令行形式运行，请输入参数!"
    print u"语法：get_suggest 文件1 文件2"
    print u"文件1为关键词存放的文件，系统会根据里面存放的关键词进行智能生成"
    print u"文件2为系统生成文件的存放位置，可以为空，为空时，系统会自动创建文件，存放在和文件1相同的位置"
    print ""
    sfile=raw_input("请输入关键词文件:".decode('utf-8').encode('gbk'))
    tfile=""
elif not(sys.argv[2:]):
    sfile=sys.argv[1]
    tfile=""
else:
    sfile=sys.argv[1]
    tfile=sys.argv[2]
#如果关键词文件不存在，退出执行
if not(os.path.isfile(sfile)):
    print u"关键词文件不存在!"
    sys.exit()
#如果目标文件不存在或输入错误，则以关键词文件为基础
if not(os.path.isfile(tfile)):
    tfile=os.path.dirname(sfile)+"/suggest.txt"
#读取源文件：
f=open(sfile,"r")
yahoo=keywords()
while 1:
    line=f.readline()
    if not line:break
    yahoo.get_search_suggest(line,tfile)
    time.sleep(1)
f.close()
