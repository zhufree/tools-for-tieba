#-*- coding:utf-8 -*-
INDEX_URL='http://www.baidu.com/'

TOKEN_URL='https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login'

LOGIN_URL='https://passport.baidu.com/v2/api/?login'

INFO_URL='http://i.baidu.com/'

ADD_THREAD_URL = 'http://tieba.baidu.com/f/commit/thread/add'

ADD_REPLY_URL='http://tieba.baidu.com/f/commit/post/add'

SIGN_URL = 'http://c.tieba.baidu.com/c/c/forum/sign'
#用来构建发帖数据的真实mouse_pwd
MOUSE_CRACK = [
        '55,61,61,41,49,48,52,53,12,52,41,53,41,52,41,53,41,52,41,53,12,49,55,53,49,60,61,51,12,52,55,61,53,41,61,53,53,',
        '119,114,124,105,113,115,114,115,76,116,105,117,105,116,105,117,105,116,105,117,105,116,105,117,105,116,105,117,76,112,117,115,125,114,117,112,76,116,119,125,117,105,125,117,117,',
        '57,56,58,38,62,63,56,57,3,59,38,58,38,59,38,58,38,59,38,58,38,59,38,58,38,59,38,58,3,59,60,61,63,57,61,3,59,56,50,58,38,50,58,58,',
        '11,11,15,20,12,11,9,0,49,9,20,8,20,9,20,8,20,9,20,8,20,9,20,8,20,9,20,8,49,13,11,11,9,13,49,9,10,0,8,20,0,8,8,',
        '16,21,20,8,16,17,22,29,45,21,8,20,8,21,8,20,8,21,8,20,45,17,23,23,19,23,45,21,22,28,20,8,28,20,20,',
        '5,14,0,27,3,4,6,4,62,6,27,7,27,6,27,7,27,6,27,7,27,6,27,7,27,6,27,7,62,6,5,6,1,7,14,3,62,6,5,15,7,27,15,7,7,',
        '7,28,25,4,28,29,24,30,33,25,4,24,4,25,4,24,4,25,4,24,4,25,4,24,4,25,4,24,33,28,16,27,29,24,33,25,26,16,24,4,16,24,24,',
        '58,56,48,37,61,60,59,57,0,56,37,57,37,56,37,57,37,56,37,57,37,56,37,57,37,56,37,57,0,63,59,63,60,57,0,56,59,49,57,37,49,57,57,',
        '112,113,115,111,119,118,113,112,74,114,111,115,111,114,111,115,111,114,111,115,111,114,111,115,111,114,111,115,74,117,119,122,116,117,74,114,113,123,115,111,123,115,115,',
        '17,21,29,9,17,16,23,17,44,20,9,21,9,20,9,21,9,20,9,21,9,20,9,21,9,20,9,21,44,17,17,29,29,16,44,20,23,29,21,9,29,21,21,'
        '17,21,29,9,17,16,23,17,44,20,9,21,9,20,9,21,9,20,9,21,9,20,9,21,9,20,9,21,44,17,17,29,29,16,44,20,23,29,21,9,29,21,21,',
    ]

HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1 WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}


