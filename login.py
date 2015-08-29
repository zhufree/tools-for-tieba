#-*- coding:utf-8 -*-
#login baidu

import cookielib
import urllib
import urllib2
import re
import gzip
import time
import random
from bs4 import BeautifulSoup
from StringIO import StringIO
from settings import *
from local_settings import *

def login_baidu(username,password):

    #prepare:load cookiejar to save cookies
    cookie_jar=cookielib.LWPCookieJar()
    cookie_support=urllib2.HTTPCookieProcessor(cookie_jar)
    opener=urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    print u'登录中...'

    #first:visit index page to get the BAIDUID,save in the cookiejar
    indexRequest = urllib2.Request(url=INDEX_URL)
    while True:
        try:
            urllib2.urlopen(indexRequest,timeout=10)
        except Exception, e:
            print e
            continue
        else:
            break
    

    #second:get token(with BAIDUID)
    tokenRequest = urllib2.Request(url=TOKEN_URL)
    while True:
        try:
            tokenResponse=urllib2.urlopen(tokenRequest,timeout=10)
        except Exception, e:
            print e
            continue
        else:
            break

    tokenInfo=tokenResponse.read()
    #print tokenInfo

    #the response forms like following
    #{"errInfo":{ "no": "0" }, 
    #   "data": { "rememberedUserName" : "", 
    #             "codeString" : "",
    #             "token" : "5b576b5d5a4afc302633c1a65d990f7a", 
    #             "cookie" : "1", "usernametype":"",
    #             "spLogin" : "rate", 
    #             "disable":"", 
    #             "loginrecord":{ 'email':[ ], 'phone':[ ] }
    #           }
    #}

    matchVal = re.search(u'"token" : "(?P<tokenVal>.*?)"',tokenInfo)
    tokenVal = matchVal.group('tokenVal')
    #print '=======token is '+tokenVal+'========='

    #visit login url and post data
    rawData={'charset':'UTF-8',
        'token':tokenVal,
        'isPhone':'false',  
        'u' : 'https://passport.baidu.com/',
        'loginType':'1',          
        'username':username,          
        'password':password, 
        'tpl':'pp',
        'staticpage':'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
        'verifycode':'nlvv',       
        'callback' : "parent.bd__pcbs__ra48vi"
        }

    post_data(rawData)

def post_data(rawData):
    postData=urllib.urlencode(rawData)
    loginRequest = urllib2.Request(LOGIN_URL,postData,HEADERS)
    loginResponse=urllib2.urlopen(loginRequest,timeout=10)
    #several ways to know whether login successful
    #print loginResponse.info()
    #first:make sure PTOKEN,STOKEN,SAVEUSERID,PASSID are in response info
    '''
    Set-Cookie: PTOKEN=deleted; expires=Sun, 20-Apr-2014 03:40:38 GMT; path=/; domai
    n=baidu.com; httponly
    Set-Cookie: PTOKEN=63cd1940a5de3737de5a8cbd02154a26; expires=Fri, 07-Jul-2023 03
    :40:39 GMT; path=/; domain=passport.baidu.com; httponly
    Set-Cookie: STOKEN=8abaecc88b5d709807e4ee18cb3589435ef9e45e511cef05689dbf5eb0aba
    291; expires=Fri, 07-Jul-2023 03:40:39 GMT; path=/; domain=passport.baidu.com; h
    ttponly
    Set-Cookie: SAVEUSERID=665821d9ac7537beb4e699e036423b36df2af9; expires=Fri, 07-J
    ul-2023 03:40:39 GMT; path=/; domain=passport.baidu.com; httponly
    Set-Cookie: USERNAMETYPE=1; expires=Fri, 07-Jul-2023 03:40:39 GMT; path=/; domai
    n=passport.baidu.com; httponly
    Set-Cookie: UBI=fi_PncwhpxZ%7ETaJc0i8bafLQmtE9sCuuORhjfZ4TYw64bmf%7EtepJH3mB3dVK
    6QPpXsNJanEq66CJo8oMEqPZl8AphK%7EMrqKcYCDyBs67DmqTaolBJTxRsSqI85Qwa7o0JZ%7E0q-aT
    67RdMT1OBBCLDCKU1e7; expires=Fri, 07-Jul-2023 03:40:39 GMT; path=/; domain=passp
    ort.baidu.com; httponly
    Set-Cookie: PASSID=SXsQAD; expires=Sun, 20-Apr-2014 03:40:39 GMT; path=/; domain
    =passport.baidu.com; httponly
    '''
    #second:the response self is a gzip file,unzip file and get the link

    buffer = StringIO(loginResponse.read())
    f = gzip.GzipFile(fileobj=buffer)
    loginResponse = f.read()
    #print loginResponse
    URL_matcher = re.search(u"encodeURI\('(?P<URL>.*?)'\)", loginResponse)
    redirectURL = URL_matcher.group('URL')
    #print redirectURL
    #the link is like following
    '''
    https://passport.baidu.com/static/passpc-account/html/v3Jump.html?hao123Param=Zz
    JhSGQzVkhjNGNGUlBNRVZMYlV0YVNYazVTa2xMUWtRdE1FTnJRblZuT1dkeVRXRlBOMlZYU2tsQlZuaF
    dRVUZCUVVGQkpDUUFBQUFBQUFBQUFBRUFBQUJYbTk4aXdhTFd2cmUwMDZiSzFBQUFBQUFBQUFBQUFBQU
    FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFFaD
    BORlZJZERSVmRq&callback=parent.bd__pcbs__ra48vi&index=0&codestring=&username=%E7
    %AB%8B%E5%BF%97%E5%8F%8D%E5%BA%94%E8%AF%95&phonenumber=&mail=&tpl=pp&u=https%3A%
    2F%2Fpassport.baidu.com%2F&needToModifyPassword=0&gotourl=&auth=&error=0
    '''
    # and notice the last "error=0",that means login successful.
    if 'error=0' in redirectURL:
        print rawData['username']+u' 登陆成功!'
        return True
    #'error=257'，需要输入验证码
    elif 'error=257' in redirectURL:
        #print redirectURL
        vcodeMatch=re.search(r'codestring=tcIcaptchaservice\S+&username',redirectURL)
        vcodeNum=vcodeMatch.group(0)[11:-9]
        rawData['codestring']=vcodeNum
        vcodeUrl='https://passport.baidu.com/cgi-bin/genimage?'+vcodeNum
        #print vcodeUrl
        vcodeRequest=urllib2.Request(vcodeUrl)
        vcodeResponse=urllib2.urlopen(vcodeRequest)
        with open('vcode.jpg','wb') as out:
            out.write(vcodeResponse.read())
            out.flush()
        vcode=raw_input(u'input vcode:')
        rawData['verifycode']=vcode
        #print rawData
        post_data(rawData)
    else:
        print u'登录失败'
        return False
    #third:visit the user's info center
    #infoRequest=urllib2.Request(url=info_url)
    #infoResponse=urllib2.urlopen(infoRequest,timeout=10)
    #with open('test.html','w') as out:
    #   out.write(infoResponse.read())#output the page to see    
    #infoPage=BeautifulSoup(infoResponse)
    #print infoPage
    #m=infoPage.find('a',attrs={'class':'ibx-uc-nick'})
    #print m.renderContents()
    #if m.renderContents()==username:
    #    return True
    #else:
    #    return False


if __name__ == '__main__':
    user=USER_LIST[4]
    login_baidu(user['username'],user['password'])