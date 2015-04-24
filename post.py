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
    def __init__(self, tiebaURL):
        self.url = tiebaURL
    def getinfo(self):
        tiebaPage =BeautifulSoup(urllib2.urlopen(self.url))
        pageContent = str(tiebaPage)
        #print pageContent
        fidPattern = re.compile(u"forumId:'(?P<fidValue>.*?)'")
        tbsPattern = re.compile(u'PageData\.tbs = \"(?P<tbsValue>.*?)\"')
        #with open('test.html','w') as out:
            #out.write(pageContent)

        fidMatch = re.search(u"\"id\":([0-9]+),\"is_like\"", pageContent)
        tbsMatch = re.search(u'PageData\.tbs = \"(?P<tbsValue>.*?)\"', pageContent)

        #some key param
        self.fid = fidMatch.group(1)
        self.tbs = tbsMatch.group('tbsValue')
        print 'fid is:',self.fid
        print 'tbs is: ',self.tbs

        #make timestamp
        self.timestamp = str(int(time.time()*1000))
        #print 'time stamp is:   ',timestamp
        self.headers = {}
        self.headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        self.headers['Accept-Encoding'] = 'gzip,deflate,sdch'
        self.headers['Accept-Language'] = 'en-US,en;q=0.5'
        self.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'


    def post(self,title,content):
        '''
        mouse_pwd is create by js,using for robot examination.
        kw is the name of the tieba.
        '''
        threadData = {

            '__type__'  :   'thread',
            'content'   :   content.encode('utf-8'),
            'fid'       :   self.fid,
            'floor_num' :   '0',
            'ie'        :   'utf-8',
            'kw'        :   kw,
            'mouse_pwd' :   mouse_crack[random.randint(0, len(mouse_crack)) - 1] + self.timestamp,
            'mouse_pwd_isclick' : '0',
            'mouse_pwd_t'   :self.timestamp,
            'rich_text' :   '1',
            'tbs'       :   self.tbs,
            'tid'       :   '0',
            'title'     :   title.encode('utf-8'),

        }


        postData = urllib.urlencode(threadData)

        postThread = urllib2.Request(add_thread_url, postData,self.headers)
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
            'kw'        :   kw,
            'mouse_pwd' :   mouse_crack[random.randint(0, len(mouse_crack)) - 1] + self.timestamp,
            'mouse_pwd_isclick' : '0',
            'mouse_pwd_t'   :self.timestamp,
            'rich_text' :   '1',
            'tbs'       :   self.tbs,
            'tid'       :   tid,#id of the post

        }

        postData = urllib.urlencode(postData)

        postThread = urllib2.Request(add_reply_url, postData,self.headers)
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

bar=Bar(tieba_url)
login_baidu("","")
bar.getinfo()
link_lst=['http://tieba.baidu.com/p/3649143599',
'http://tieba.baidu.com/p/3600373274',
'http://tieba.baidu.com/p/3492845027',
'http://tieba.baidu.com/p/3508624708',
'http://tieba.baidu.com/p/3037083498']
for i in link_lst:
    bar.reply('reply test',i)
#bar.reply('[4.23]test',"http://tieba.baidu.com/p/3716708841")
