# -*- coding: utf-8 -*-
from login import *
from post import *
from setting import *
from snatch import *
'''
username=raw_input("username:")
password=raw_input("password")
'''
username=''
password=''
login_baidu(username, password)
'''
tieba_url=raw_input("tieba_url:")
kw=raw_input("tieba_name:")
'''
tieba_url='http://tieba.baidu.com/f?kw=%B7%B4%D3%A6%CA%D4%BD%CC%D3%FD'
#tieba_url='http://tieba.baidu.com/f?kw=%E6%9C%B1%E5%AD%90%E5%AE%A5&ie=utf-8'
#kw='朱子宥'
kw='反应试教育'
bar=Bar(tieba_url,kw)
bar.getinfo()
article_to_post_url='http://mp.weixin.qq.com/s?__biz=MzA4MTU3NTQzMg==&mid=207407103&idx=3&sn=38378b00045fa3dcff406c7934e66e52#rd'
#post_=getcontent(article_to_post_url)
'''
post_title=raw_input("title:")
post_content=raw_input("content:")
'''
#bar.post(post_['title'], post_['content'])
'''
reply_url=raw_input("reply_url:")
reply_content=raw_input("content:")
'''
#bar.reply(reply_content, reply_url)
