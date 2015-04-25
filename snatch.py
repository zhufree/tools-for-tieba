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
        post_['title']=title
        paras= soup.find_all("p") 
        for p in paras:
            if p.next.string!=None:
                sentence=p.next.string.encode('utf-8')
                if sentence!="已评论" and sentence!= "微信扫一扫":
                    content+=sentence
                    content+="\n"*2
        with open('text.txt','w') as out:
            out.write(title)
            out.write(content)#output the page to see   
        post_['content']=content 
        return post_

