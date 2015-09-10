# -*- coding: utf-8 -*-
from login import *
from post import *
from local_settings import *
from snatch import *
import time


def post_article_with_many_paragraphs(user_list,article_url,tieba_url):
	#set user and login
	user=user_list[1]
	login_baidu(user['username'], user['password'])

	#set tieba
	bar=Bar(tieba_url)
	bar.getinfo()

	#set article to post
	post_=get_from_wechat(article_url)
	print post_['content']
	#post the first paragraph as first floor
	post_result=bar.post(post_['title'], post_['content'][0])
	while(post_result==False):#if post failed,try again
		time.sleep(10)
		post_result=bar.post(post_['title'], post_['content'][0])

	tid=post_result#get id of the post,reply next paragraphs as reply
	print tid
	for i in range(2,len(post_['content'])):
		print i
		try:
			#print post_['content'][i]
			#result=bar.reply(post_['content'][i], tid)
			while(result==False):
				time.sleep(20)
				#result=bar.reply(post_['content'][i], tid)
			time.sleep(10)
		except Exception, e:
			print e
			break
		else:
			pass

def up_to_many_post(tid_list):

	for t in tid_list:
		curBar=Bar(t['bar_url'])
		curBar.getinfo()
		curBar.reply(' xx',t['tid'])
		time.sleep(30)


if __name__ == '__main__':
	user=USER_LIST[4]
	#while login_baidu(user['username'],user['password'])!=True:
	login_baidu(user['username'],user['password'])
	#while True:
		#login_baidu(user['username'],user['password'])
		#up_to_many_post(TO_UP_LIST)
		#time.sleep(30)