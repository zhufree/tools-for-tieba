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

def post(title,content,tiebaURL):
    login_baidu(username,password)
    tiebaPage =BeautifulSoup(urllib2.urlopen(tiebaURL))
    pageContent = str(tiebaPage)
    #print pageContent
    fidPattern = re.compile(u"forumId:'(?P<fidValue>.*?)'")
    tbsPattern = re.compile(u'PageData\.tbs = \"(?P<tbsValue>.*?)\"')
    #with open('test.html','w') as out:
        #out.write(pageContent)

    fidMatch = re.search(u"\"id\":([0-9]+),\"is_like\"", pageContent)
    tbsMatch = re.search(u'PageData\.tbs = \"(?P<tbsValue>.*?)\"', pageContent)

    #some key param
    fid = fidMatch.group(1)
    tbs = tbsMatch.group('tbsValue')
    #print 'fid is:',fid
    #print 'tbs is: ',tbs

    #make timestamp
    timestamp = str(int(time.time()*1000))
    #print 'time stamp is:   ',timestamp

    '''
    mouse_pwd is create by js,using for robot examination.
    kw is the name of the tieba.
    '''

    threadData = {

        '__type__'  :   'thread',
        'content'   :   content.encode('utf-8'),
        'fid'       :   fid,
        'floor_num' :   '0',
        'ie'        :   'utf-8',
        'kw'        :   '反应试教育',
        'mouse_pwd' :   mouse_crack[random.randint(0, len(mouse_crack)) - 1] + timestamp,
        'mouse_pwd_isclick' : '0',
        'mouse_pwd_t'   :   timestamp,
        'rich_text' :   '1',
        'tbs'       :   tbs,
        'tid'       :   '0',
        'title'     :   title.encode('utf-8'),

    }

    headers = {}
    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Accept-Encoding'] = 'gzip,deflate,sdch'
    headers['Accept-Language'] = 'en-US,en;q=0.5'
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    postData = urllib.urlencode(threadData)

    postThread = urllib2.Request(ADD_THREAD, postData,headers)
    #send = urllib2.urlopen(postThread)
    #buffer = StringIO( send.read())
    #f = gzip.GzipFile(fileobj=buffer)
    #postResponse = f.read()
    #print postResponse


post('[4.22]test','test-----from my windows cmd','http://tieba.baidu.com/f?kw=%B7%B4%D3%A6%CA%D4%BD%CC%D3%FD')