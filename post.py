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
            print 'Post successful!'
            return True
        else:
            print 'Fail to post_(:з」∠)_'
            return False

    def reply(self,content,tie_url):
        tidMatch = re.search(r"\d+", tie_url)
        tid = tidMatch.group(0)
        postData = {

            '__type__'  :   'reply',
            'content'   :   content.encode('utf-8'),
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
            print 'Post successful!'
            return True
        else:
            print 'Fail to post_(:з」∠)_'
            return False

#bar=Bar(tieba_url)
#bar.getinfo()
link_lst=[
'http://tieba.baidu.com/p/3600373274',
'http://tieba.baidu.com/p/3492845027',
'http://tieba.baidu.com/p/3508624708',
]
#bar.reply('[4.23]test',"http://tieba.baidu.com/p/3716708841")
