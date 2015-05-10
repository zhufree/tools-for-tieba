#-*- coding:utf-8 -*-
#post thread auto

from bs4 import BeautifulSoup
import cookielib
import urllib
import urllib2
import re
import gzip
import time
import random
from datetime import datetime
from StringIO import StringIO
from setting import *

from login import *

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

tieba_url=''


class Bar(object):
    """docstring for Bar"""
    def __init__(self, tiebaURL,kw):
        self.url = tiebaURL
        self.kw=kw
    def getinfo(self):
        tiebaPage =BeautifulSoup(urllib2.urlopen(self.url))
        pageContent = str(tiebaPage)
        #print pageContent

        #with open('test.html','w') as out:
            #out.write(pageContent)

        fidMatch = re.search(u"\"forum_id\":([0-9]+),", pageContent)
        tbsMatch = re.search(u'PageData\.tbs = \"(?P<tbsValue>.*?)\"', pageContent)

        #some key param
        self.fid = fidMatch.group(1)
        self.tbs = tbsMatch.group('tbsValue')
        print 'fid is:',self.fid
        print 'tbs is: ',self.tbs

        #make timestamp
        self.timestamp = str(int(time.time()*1000))
        #print 'time stamp is:   ',timestamp

    def get_user_id(self):
        '''get list of user id of who like tieba'''
        print u'获取吧友id...'
        page_count = 1
        users_like_tieba = []
        f=open('userid.txt','w')
        while True:
            user_url='http://tieba.baidu.com/f/like/furank?kw=%s&ie=utf-8&pn=%d' % (self.kw,page_count)
            idRequest = urllib2.Request(user_url)
            idSoup=BeautifulSoup(urllib2.urlopen(idRequest))
            temp_like_tieba =[]
            divs=idSoup.find_all('div',{'class':'drl_item_card'})
            for div in divs:
                f.writelines(div.next.renderContents()+'\n')
                temp_like_tieba.append(div.next.renderContents())
            if not temp_like_tieba:
                break
            if not users_like_tieba:
                users_like_tieba = temp_like_tieba
            else:
                users_like_tieba += temp_like_tieba
            page_count += 1
        f.close()
        return users_like_tieba

    def post(self,title,content):
        '''
        mouse_pwd is create by js,using for robot examination.
        kw is the name of the tieba.
        '''
        threadData = {

            '__type__'  :   'thread',
            'content'   :   content,
            'fid'       :   self.fid,
            'floor_num' :   '0',
            'ie'        :   'utf-8',
            'kw'        :   self.kw,
            'mouse_pwd' :   mouse_crack[random.randint(0, len(mouse_crack)) - 1] + self.timestamp,
            'mouse_pwd_isclick' : '0',
            'mouse_pwd_t'   :self.timestamp,
            'rich_text' :   '1',
            'tbs'       :   self.tbs,
            'tid'       :   '0',
            'title'     :   title,

        }


        postData = urllib.urlencode(threadData)

        postThread = urllib2.Request(add_thread_url, postData,headers)
        send = urllib2.urlopen(postThread)
        buffer = StringIO( send.read())
        f = gzip.GzipFile(fileobj=buffer)
        postResponse = f.read()
        #print postResponse
        #the postResponse is like below
        '''
        {"no":0,
        "err_code":0,
        "error":"",
        "data":{
            "autoMsg":"",
            "fid":1414011,
            "fname":"\u53cd\u5e94\u8bd5\u6559\u80b2",
            "tid":3719935150,"is_login":1,
            "content":"test-----from my windows cmd",
            "vcode":{
                "need_vcode":0,
                "str_reason":"",
                "captcha_vcode_str":"",
                "captcha_code_type":0,
                "userstatevcode":0
                }
            }
        }
        '''
        if "\"err_code\":0" in postResponse:
            tidMatch = re.search(u"\"tid\":([0-9]+),", postResponse)
            self.tid=tidMatch.group(1)
            print u'发帖成功，帖子id是：'+self.tid
            return self.tid
        else:
            print u'发帖失败'
            return False

    def reply(self,content,tid):
        postData = {

            '__type__'  :   'reply',
            'content'   :   content,
            'fid'       :   self.fid,
            #'floor_num' :   '8',
            'ie'        :   'utf-8',
            'kw'        :   self.kw,
            'mouse_pwd' :   mouse_crack[random.randint(0, len(mouse_crack)) - 1] + self.timestamp,
            'mouse_pwd_isclick' : '0',
            'mouse_pwd_t'   :self.timestamp,
            'rich_text' :   '1',
            'tbs'       :   self.tbs,
            'tid'       :   tid,#id of the post

        }

        postData = urllib.urlencode(postData)

        postThread = urllib2.Request(add_reply_url, postData,headers)
        send = urllib2.urlopen(postThread)
        buffer = StringIO( send.read())
        f = gzip.GzipFile(fileobj=buffer)
        postResponse = f.read()
        #print postResponse
        if "\"err_code\":0" in postResponse:
            print u'回帖成功!'
            return True
        else:
            print u'回帖失败'
            return False

    def at_all_user(self,tid):
        f=open('userid.txt','r')
        while f.readline():
            reply=u''
            count=0
            while count<5:#回一次贴最多只能艾特5个
                tmp_user='@'+f.readline().rstrip()+' '
                reply+=tmp_user
                count+=1
            print reply
            result=bar.reply(reply,tid)
            time.sleep(10)
            while result!=True:
                time.sleep(60)
                result=bar.reply(reply,tid)

login_baidu('','')
bar=Bar(tieba_url,'')
bar.getinfo()
bar.get_user_id()
bar.at_all_user('')

