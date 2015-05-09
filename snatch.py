# -*- coding: utf-8 -*-
import urllib2 
from bs4 import BeautifulSoup
import re

def get_from_wechat(url):
    post_={}
    content=""
    try:
        soup = BeautifulSoup(urllib2.urlopen(url, timeout=4))
    except Exception:
        pass
    else:
        title=soup.find("h2").string.encode('utf-8')
        post_['title']=u'【转】'+title
        post_['content']=[]
        f=open('text.txt','w')
        f.write(title)
        paras= soup.find_all("p") 
        for p in paras:
            if p.next.string!=None:
                sentence=p.next.string
                #sentence=unicode(p.next.string,'utf-8')
                #print sentence
                if sentence not in ["已评论","微信扫一扫"," ","　","　　"]:
                    f.write(sentence)
                    post_['content'].append(sentence)
        f.close()
        return post_

def get_from_paomianba(url):
    post_={}
    content=""
    try:
        soup = BeautifulSoup(urllib2.urlopen(url, timeout=4))
    except Exception,e:
        print e
    else:
        title=soup.find_all('a',{'rel':'bookmark'})[0].string.encode('utf-8')
        print title
        post_['title']='【转】'+title
        post_['content']=[]
        f=open('text.txt','w')
        f.write(title)
        paras= soup.find_all("p") 
        for p in paras:
            if p.strong:
                sentence=p.strong.renderContents()
            elif p.span:
                sentence='作者'+p.next.next.next.renderContents()
            elif p.a:
                pass
            else:
                sentence=p.renderContents()
                #sentence=unicode(p.next.string,'utf-8')
            print sentence
            f.write(sentence)
            post_['content'].append(sentence)
        f.close()
        return post_
get_from_paomianba('http://www.paomianba.com/2015/04/29/242.html')