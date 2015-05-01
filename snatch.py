# -*- coding: utf-8 -*-
import urllib2 
from bs4 import BeautifulSoup
import re
def getcontent(url):
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

