#-*- coding:utf-8 -*-

import cookielib
import re
import gzip
import time
import random
import json
import hashlib
from StringIO import StringIO

from bs4 import BeautifulSoup
import requests

from settings import *
from local_settings import *

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def has_title_but_no_class(tag):
        return tag.has_attr('title') and not tag.has_attr('class')

class Account(object):

    """Login Baidu Account, Collect Info And Sign. """

    def __init__(self, username, password):

        """ login """

        self.username = username
        self.password = password
        self.like_tiebas = [] 
        # self.login_baidu()
        self.session = requests.Session()
        try:
            load_cookiejar = cookielib.LWPCookieJar()
            load_cookiejar.load('cookies/' + self.username + '.txt', ignore_discard=True, ignore_expires=True)
            load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
            self.session.cookies = requests.utils.cookiejar_from_dict(load_cookies)
            print 'use cookiejar'
        except Exception, e:
            self.login_baidu()
        finally:
            if self.visit_page():
                self.like_tiebas = [] 
            else:
                self.login_baidu()

    def login_baidu(self):

        """
        use username and password to login
        :param username: baidu ID, not phonenumber or email
        :param password: pasword
        :return: True or False
        """

        # prepare:load cookiejar to save cookies
        new_cookie_jar = cookielib.LWPCookieJar(self.username + '.txt')
        
        print u'Login...'

        # first:visit index page to get the BAIDUID,save in the cookiejar
        idx_req = self.session.get(INDEX_URL)

        # second:get token(with BAIDUID)
        token_req = self.session.get(TOKEN_URL)

        token_info = token_req.text
        # print token_info

        # the response forms like following
        # {"errInfo":{ "no": "0" },
        #   "data": { "rememberedUserName" : "",
        #             "codeString" : "",
        #             "token" : "5b576b5d5a4afc302633c1a65d990f7a",
        #             "cookie" : "1", "usernametype":"",
        #             "spLogin" : "rate",
        #             "disable":"",
        #             "loginrecord":{ 'email':[ ], 'phone':[ ] }
        #           }
        # }

        matchVal = re.search(u'"token" : "(?P<tokenVal>.*?)"', token_info)
        tokenVal = matchVal.group('tokenVal')
        # print '=======token is '+tokenVal+'========='

        # visit login url and post data
        postData = {
            'charset': 'UTF-8',
            'token': tokenVal,
            'isPhone': 'false',
            'u': 'https://passport.baidu.com/',
            'loginType': '1',
            'username': self.username,
            'password': self.password,
            'tpl': 'pp',
            'staticpage': 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
            'verifycode': 'nlvv',
            'callback': "parent.bd__pcbs__ra48vi"
        }

        self.post_data(postData, new_cookie_jar)

    def post_data(self, postData, new_cookie_jar):
        """ 
        post data to login
        :param postData: raw data dict.
        :return: True or False
        """
        login_req = self.session.post(LOGIN_URL, postData)
        # several ways to know whether login successful

        # first:make sure PTOKEN,STOKEN,SAVEUSERID,PASSID are in response info
        # print login_req.cookies.keys()

        # second:the response self is a gzip file,unzip file and get the link
        # print login_req.text

        # "error=0",that means login successful.
        if 'error=0' in login_req.text:
            requests.utils.cookiejar_from_dict({c.name: c.value for c in self.session.cookies}, new_cookie_jar)
            new_cookie_jar.save('cookies/' + self.username + '.txt', ignore_discard=True, ignore_expires=True)
            print postData['username']+' logged in!'
            return True
        #'error=257'，need to input verifycode
        elif 'error=257' in login_req.text:
            # print redirectURL
            # match verify code
            vcodeMatch = re.search(r'codestring=\S+&username', login_req.text)
            
            # cut the string
            vcodeNum = vcodeMatch.group(0)[11:-9]
            # print vcodeNum
            # add into the post data
            postData['codestring'] = vcodeNum
            # get vcode img url
            vcodeUrl = 'https://passport.baidu.com/cgi-bin/genimage?' + \
                vcodeNum
            # print vcodeUrl
            vcode_req = requests.get(vcodeUrl)
            # download the vcode img
            with open('vcode.jpg', 'wb') as out:
                out.write(vcode_req.content)
                out.flush()
            # input vcode
            vcode = raw_input(u'input vcode:')
            postData['verifycode'] = vcode
            # post data again
            self.post_data(postData, new_cookie_jar)
        else:
            print u'登录失败'
            return False  

    def get_bars(self):
        """
        get bars that account like
        :need login first
        :return: self.like_tiebas:a list contain tieba that user likes, each format is :
        {
            'name': 'XXXXXX',
            'link': 'http://tieba.baidu.com/?f=xxxxxx'
        }
        """
        page_count = 1
        while True:
            if self.visit_page(page_count):
                pass
            else:
                break
            page_count += 1
        print 'get ' + str(len(self.like_tiebas)) + ' bars'
        return self.like_tiebas

    def visit_page(self, page_id=1):
        """
        visit like tieba page to get tieba
        :param page_id: page id of the like tieba list, default 1
        :return: self.like_tiebas
        """
        like_tieba_url = 'http://tieba.baidu.com/f/like/mylike?&pn=%d' % page_id
        fetch_req = self.session.get(like_tieba_url)
        fetchPage = BeautifulSoup(fetch_req.text, "lxml")
        # print fetchPage
        bar_boxs = fetchPage.find_all(has_title_but_no_class)
        if bar_boxs:
            temp_like_tieba = [{
                'name': bar['title'].encode('utf-8'),
                'link':'http://tieba.baidu.com'+bar['href']
            } for bar in bar_boxs]
            # each bar is a dict with name and link
            if temp_like_tieba:
                if not self.like_tiebas:
                    self.like_tiebas = temp_like_tieba
                else:
                    self.like_tiebas += temp_like_tieba
                return True
            else:
                return False
        else:
            return False

    def fetch_tieba_info(self):
        """
        get info about each tieba and sign
        :need login first
        :param self.like_tiebas:
        :return: list contains info of a bar, each format like:
        {
            'sign_status':[] or ['xxxx'],
            'tbs': 'xxxxxx',
            'fid': 'xxxxxx'
        }
        """
        self.like_tiebas_info = []
        for tieba_info in self.like_tiebas:
            tieba_wap_url = "http://tieba.baidu.com/mo/m?kw=" + tieba_info['name']
            wap_req = self.session.get(tieba_wap_url)
            re_already_sign = '<td style="text-align:right;"><span[ ]>(.*?)<\/span><\/td><\/tr>'
            if re.findall(re_already_sign, wap_req.text):
                tieba_info['sign_status'] = True
            else:
                tieba_info['sign_status'] = False
            re_fid = '<input type="hidden" name="fid" value="(.+?)"\/>'
            _fid = re.findall(re_fid, wap_req.text)
            tieba_info['fid'] = _fid and _fid[0] or None
            re_tbs = '<input type="hidden" name="tbs" value="(.+?)"\/>'
            _tbs = re.findall(re_tbs, wap_req.text)
            tieba_info['tbs'] = _tbs and _tbs[0] or None
            self.like_tiebas_info.append(tieba_info)
        # print self.like_tiebas_info
        return self.like_tiebas_info

    def auto_sign(self):
        """ 
        auto sign function 
        :need login first
        :param self.like_tiebas_info:
        :return self.like_tiebas_info: change the sign_status in self.like_tiebas_info
        """
        for tieba_info in self.like_tiebas_info:
            if tieba_info['sign_status']:
                pass
            else:
                tieba_info['sign_status'] = self.sign(
                    tieba_info['fid'], 
                    tieba_info['tbs'], 
                    tieba_info['name']
                    )
        return self.like_tiebas_info

    def sign(self, fid, tbs, kw):
        """
        do sign 
        :param fid, tbs, kw: info of a bar
        """
        sign_post_data = {
            "_client_id": "03-00-DA-59-05-00-72-96-06-00-01-00-04-00-4C-43-01-00-34-F4-02-00-BC-25-09-00-4E-36",
            "_client_type": "4",
            "_client_version": "1.2.1.17",
            "_phone_imei": "540b43b59d21b7a4824e1fd31b08e9a6",
            "fid": fid,
            "kw": kw,
            "net_type": "3",
            'tbs': tbs
        }

        sign_post_data = self._decode_uri_post(sign_post_data)

        sign_req = self.session.post(SIGN_URL, data=sign_post_data)
        sign_dict = eval(sign_req.content)
         
        error_code = sign_dict['error_code']
        sign_bonus_point = 0
        try:
            # Don't know why but sometimes this will trigger key error.
            sign_bonus_point = int(
                sign_dict['user_info']['sign_bonus_point'])
        except KeyError:
            pass
        if error_code == '0':
            print kw+u"吧 签到成功,经验+%d" % sign_bonus_point
            return True
        else:
            print u'签到失败'
            # print "Error:" + unicode(error_code) + " " +
            # unicode(error_msg)
            return False


    def _decode_uri_post(self, postData):
        """
        decode post data
        tool function, use when sign.
        :param postData: data to post when sign.
        :return: decoded data.
        """

        SIGN_KEY = "tiebaclient!!!"
        s = ""
        keys = postData.keys()
        keys.sort()
        for i in keys:
            s += i + '=' + postData[i]
        sign = hashlib.md5(s + SIGN_KEY).hexdigest().upper()
        postData.update({'sign': str(sign)})
        return postData


if __name__ == '__main__':
    for user in USER_LIST[1:]:
        user = Account(user['username'], user['password'])
        user.get_bars()
        user.fetch_tieba_info()
        user.auto_sign()
        # for i in user.like_tiebas_info:
        #     if i['sign_status']:
        #         pass
        #     else:
        #         print i
        print 'end:' + user.username
    print 'end all'
