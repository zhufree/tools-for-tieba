# -*- coding: utf-8 -*-
from login import *
from post import *
from setting import *
from snatch import *

#set username and password
username='立志反应试'
password='15256654206'
login_baidu(username, password)

#set tieba url and kw(name in chinese)
tieba_url='http://tieba.baidu.com/f?kw=%B7%B4%D3%A6%CA%D4%BD%CC%D3%FD'
#tieba_url='http://tieba.baidu.com/f?kw=%E6%9C%B1%E5%AD%90%E5%AE%A5&ie=utf-8'
#kw='朱子宥'
kw='反应试教育'
bar=Bar(tieba_url,kw)
bar.getinfo()
#set article to post
article_to_post_url='http://mp.weixin.qq.com/s?__biz=MzA3MTAwODgzOQ==&mid=205326269&idx=4&sn=9549453289de094033eeafbad719aef3#rd'
post_=get_from_wechat(article_to_post_url)
print len(post_['content'])
#post the first paragraph as first floor
post_result=bar.post(post_['title'], post_['content'][0])
while(post_result==False):#if post failed,try again
	post_result=bar.post(post_['title'], post_['content'][0])

tid=post_result#get id of the post,reply next paragraphs as reply
#tid='3750930653'
print tid
for i in range(2,7):
	print i
	try:
		print post_['content'][i]
		result=bar.reply(post_['content'][i], tid)
		while(result==False):
			result=bar.reply(post_['content'][i], tid)
	except Exception, e:
		print e
		break
	else:
		pass

