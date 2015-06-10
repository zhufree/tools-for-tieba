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
from settings import *
from local_settings import *
from login import *

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class Bar(object):
    """docstring for Bar"""
    def __init__(self, tiebaURL):
        self.url = tiebaURL
    def getinfo(self):
        tiebaPage =BeautifulSoup(urllib2.urlopen(self.url))
        pageContent = str(tiebaPage)
        #print pageContent

        with open('test.html','w') as out:
            out.write(pageContent)

        fidMatch = re.search(u"\"forum_id\":([0-9]+),", pageContent)
        tbsMatch = re.search(u'PageData\.tbs = \"(?P<tbsValue>.*?)\"', pageContent)
        #kwMatch =re.search(u'PageData.forum.name = \'(?P<kwValue>.*?)\'', pageContent)
        titleStr=tiebaPage.find('title').string.replace('吧_百度贴吧','')
        #some key param
        self.fid = fidMatch.group(1)
        self.tbs = tbsMatch.group('tbsValue')
        self.kw=titleStr
        #print 'fid is:',self.fid
        #print 'tbs is: ',self.tbs
        #print 'kw is:',self.kw

        #make timestamp
        self.timestamp = str(int(time.time()*1000))
        #print 'time stamp is:   ',timestamp

    def get_user_id(self):
        '''get list of user id of who like tieba'''
        print u'获取吧友id...'
        page_count = 1 #count from first page
        f=open('userid.txt','w')
        while True:
            user_url='http://tieba.baidu.com/f/like/furank?kw=%s&ie=utf-8&pn=%d' % (self.kw,page_count)
            idRequest = urllib2.Request(user_url)
            idSoup=BeautifulSoup(urllib2.urlopen(idRequest))
            divs=idSoup.find_all('div',{'class':'drl_item_card'})#find 
            for div in divs:
                f.writelines(div.next.renderContents()+'\n')
            if not divs:
                break
            page_count += 1
        f.close()
        print '完成'
        return True

    def post(self,title,content):
        '''
        mouse_pwd is create by js,using for robot examination.
        kw is the name of the tieba.
        '''
        threadData = {

            '__type__'  :   'thread',
            'title'     :   title,
            'content'   :   content,
            'fid'       :   self.fid,
            'floor_num' :   '0',
            'ie'        :   'utf-8',
            'kw'        :   self.kw,
            'mouse_pwd' :   MOUSE_CRACK[random.randint(0, len(MOUSE_CRACK)) - 1] + self.timestamp,
            'mouse_pwd_isclick' : '0',
            'mouse_pwd_t'   :self.timestamp,
            'rich_text' :   '1',
            'tbs'       :   self.tbs,
            'tid'       :   '0',
        }
        postData = urllib.urlencode(threadData)
        postThread = urllib2.Request(ADD_THREAD_URL, postData,HEADERS)
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
            'mouse_pwd' :   MOUSE_CRACK[random.randint(0, len(MOUSE_CRACK)) - 1] + self.timestamp,
            'mouse_pwd_isclick' : '0',
            'mouse_pwd_t'   :self.timestamp,
            'rich_text' :   '1',
            'tbs'       :   self.tbs,
            'tid'       :   tid,#id of the post

        }
        postData = urllib.urlencode(postData)
        postThread = urllib2.Request(ADD_REPLY_URL, postData,HEADERS)
        send = urllib2.urlopen(postThread)
        buffer = StringIO( send.read())
        f = gzip.GzipFile(fileobj=buffer)
        postResponse = f.read()
        print postResponse
        if "\"err_code\":0" in postResponse:
            print u'回帖成功!'
            return True
        else:
            print u'回帖失败'
            return False

    def at_all_user(self,tid):
        f=open('userid.txt','r')
        while f.readline():#once nextline exist
            reply=u''
            count=0
            while count<5:#回一次贴最多只能艾特5个
                tmp_user='@'+f.readline().rstrip()+' '#add @ and space
                reply+=tmp_user#add to reply content
                count+=1
            #print reply
            result=bar.reply(reply,tid)#reply in thread
            time.sleep(20)
            while result!=True:#once fail to reply ,sleep for a long time
                time.sleep(60)
                result=bar.reply(reply,tid)

if __name__=='__main__':
    login_baidu(USER_LIST[4]['username'],USER_LIST[4]['password'])
    bar=Bar('http://tieba.baidu.com/f?ie=utf-8&kw=%E9%AB%98%E4%B8%89')
    bar.getinfo()
    bar.reply('up','3816192696')
    #bar.get_user_id()
    #bar.at_all_user('')

