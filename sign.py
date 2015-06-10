#-*- coding:utf-8 -*-
#sign auto
#refer to https://github.com/skyline75489/baidu-tieba-auto-sign/blob/master/baidu-tieba-auto-sign.py

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
import json
import hashlib
from login import *
from local_settings import *
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class User(object):
    """docstring for User"""
    def __init__(self, username,password):
        self.username = username
        self.password=password
        self.login_status=login_baidu(username, password)#initial user class and login
        while self.login_status!=True:
            self.login_status=login_baidu(username, password)

    def fetch_like_tieba_list(self):
        '''get list of like tiebe'''
        print u'获取喜欢的贴吧ing...'
        page_count = 1
        find_like_tieba = []
        while True:
            like_tieba_url = 'http://tieba.baidu.com/f/like/mylike?&pn=%d' % page_count
            fetchRequest = urllib2.Request(like_tieba_url)
            fetchResponse = urllib2.urlopen(fetchRequest).read()
            fetchResponse = fetchResponse.decode('gbk').encode('utf8')
            re_like_tieba = '<a href="\/f\?kw=.*?" title="(.*?)">.+?<\/a><\/td><td><a class="cur_exp" target="_blank".*?'
            temp_like_tieba = re.findall(re_like_tieba, fetchResponse)
            if not temp_like_tieba:
                break
            if not find_like_tieba:
                find_like_tieba = temp_like_tieba
            else:
                find_like_tieba += temp_like_tieba
            page_count += 1
        return find_like_tieba

    def fetch_tieba_info_and_sign(self,tieba_list):
        '''get info about each tieba and sign'''
        for tieba in tieba_list:
            info={}
            info['kw']=tieba
            tieba_wap_url = "http://tieba.baidu.com/mo/m?kw=" + tieba
            wap_resp = urllib2.urlopen(tieba_wap_url).read()
            if not wap_resp:
                pass
            re_already_sign = '<td style="text-align:right;"><span[ ]>(.*?)<\/span><\/td><\/tr>'
            info['sign_status']= re.findall(re_already_sign, wap_resp)
            re_fid = '<input type="hidden" name="fid" value="(.+?)"\/>'
            _fid = re.findall(re_fid, wap_resp)
            info['fid'] = _fid and _fid[0] or None
            re_tbs = '<input type="hidden" name="tbs" value="(.+?)"\/>'
            _tbs = re.findall(re_tbs, wap_resp)
            info['tbs'] = _tbs and _tbs[0] or None
            #print info
            try:
                self.sign(info)
                #print "here"
            except Exception, e:
                print e,info
                continue


    def _decode_uri_post(self,postData):
        '''decode post data'''
        SIGN_KEY = "tiebaclient!!!"
        s = ""
        keys = postData.keys()
        keys.sort()
        for i in keys:
            s += i + '=' + postData[i]
        sign = hashlib.md5(s + SIGN_KEY).hexdigest().upper()
        postData.update({'sign': str(sign)})
        return postData

    def sign(self,tieba_info):
        if tieba_info['sign_status']:
            print tieba_info['kw']+u'吧 之前已签到'
            return True
        else:
            sign_post_data = {
                "_client_id": "03-00-DA-59-05-00-72-96-06-00-01-00-04-00-4C-43-01-00-34-F4-02-00-BC-25-09-00-4E-36", 
                "_client_type":"4", 
                "_client_version": "1.2.1.17", 
                "_phone_imei": "540b43b59d21b7a4824e1fd31b08e9a6", 
                "fid": tieba_info['fid'], 
                "kw": tieba_info['kw'], 
                "net_type": "3", 
                'tbs': tieba_info['tbs']
            }

            sign_post_data = self._decode_uri_post(sign_post_data)
            postData = urllib.urlencode(sign_post_data)

            signRequest = urllib2.Request(SIGN_URL,postData)
            signResponse = urllib2.urlopen(signRequest, timeout=5)
            signResponse = json.load(signResponse)
            #print signResponse
            error_code = signResponse['error_code']
            sign_bonus_point = 0
            try:
            # Don't know why but sometimes this will trigger key error.
                sign_bonus_point = int(signResponse['user_info']['sign_bonus_point'])
            except KeyError:
                pass
            if error_code == '0':
                print tieba_info['kw']+u"吧 签到成功,经验+%d" % sign_bonus_point
            else:
                error_msg = signResponse['error_msg']
                if error_msg == u'亲，你之前已经签过了':
                    print u'之前已签到'
                    return True
                else:
                    print u'签到失败'
                    print "Error:" + unicode(error_code) + " " + unicode(error_msg)
                    return False




if __name__=='__main__':
	for user in USER_LIST:
	    user=User(user['username'],user['password'])
	    tb=user.fetch_like_tieba_list()
	    user.fetch_tieba_info_and_sign(tb)