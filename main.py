# -*- coding: utf-8 -*-
from login import *
from post import *
from local_settings import *
from snatch import *
import time
#set user and login
user=USER_LIST[0]
login_baidu(user['username'], user['password'])

#set tieba
bar=Bar(FYS_URL)
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
			time.sleep(20)
			result=bar.reply(post_['content'][i], tid)
		time.sleep(10)
	except Exception, e:
		print e
		break
	else:
		pass

