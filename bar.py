#-*- coding:utf-8 -*-

import cookielib
import urllib
import urllib2
import re
import gzip
import time
import random
from datetime import datetime
from StringIO import StringIO

from bs4 import BeautifulSoup

from settings import *
from local_settings import *
from account import Account


class Bar(object):

    """Get Info Of A Bar,Do Post And Reply"""

    def __init__(self, tiebaurl, user):
        self.url = tiebaurl
        self.session = user.session

    def get_info(self):
        """ get fid and tbs of a certian bar """
        tieba_req = self.session.get(self.url)
        tiebaPage = BeautifulSoup(tieba_req.text, 'lxml')
        
        # print tieba_req.text
        # with open('test.html','w') as out:
        # out.write(tieba_req.text)

        fidMatch = re.search(u"\"forum_id\":([0-9]+),", tieba_req.text)
        tbsMatch = re.search(
            u'PageData\.tbs = \"(?P<tbsValue>.*?)\"', tieba_req.text)

        # some key param
        self.fid = fidMatch.group(1)
        self.tbs = tbsMatch.group('tbsValue')
        self.kw = tiebaPage.find('title').string.replace('吧_百度贴吧', '')
        # print 'fid is:',self.fid
        # print 'tbs is: ',self.tbs

        # make timestamp
        self.timestamp = str(int(time.time() * 1000))
        # print 'time stamp is:   ',timestamp

    def get_user_id(self):
        """
        get list of user id of who like tieba
        :return:A list contain userid,as well as a txt file
        """
        # print u'获取吧友id...'
        page_count = 1
        # count from first page
        f = open(slef.kw+'userid.txt', 'w+')
        user_list = []
        while True:
            user_url = 'http://tieba.baidu.com/f/like/furank?kw=%s&ie=utf-8&pn=%d' % (
                self.kw, page_count)
            id_req = self.session.get(user_url)
            idSoup = BeautifulSoup(id_req.text, 'lxml')
            divs = idSoup.find_all('div', {'class': 'drl_item_card'})  # find
            user_list += [div.next.renderContents().encode('utf-8')
                          for div in divs]
            f.writelines(','.join(user_list))
            if not divs:
                break
            page_count += 1
        f.close()
        # print '完成'
        return user_list

    def post(self, title, content):
        """
        mouse_pwd is create by js,using for robot examination.
        kw is the name of the tieba.
        :param title:title of the post.
        :param content:content of the post
        :return:the tid of postThread, or false if post fialed.
        """
        threadData = {
            '__type__': 'thread',
            'title': title,
            'content': content,
            'fid': self.fid,
            'floor_num': '0',
            'ie': 'utf-8',
            'kw': self.kw,
            'mouse_pwd': MOUSE_CRACK[random.randint(0, len(MOUSE_CRACK)) - 1] + self.timestamp,
            'mouse_pwd_isclick': '0',
            'mouse_pwd_t': self.timestamp,
            'rich_text': '1',
            'tbs': self.tbs,
            'tid': '0',
        }
        post_req = self.session.post(ADD_THREAD_URL, data=threadData)
        postResponse = post_req.text
        # print postResponse
        # the postResponse is like below
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
        if "\"err_code\":0" in post_req.text:
            tidMatch = re.search(u"\"tid\":([0-9]+),", post_req.text)
            self.tid = tidMatch.group(1)
            print u'发帖成功，帖子id是：'+self.tid
            return self.tid
        else:
            print u'发帖失败'
            return False

    def reply(self, content, tid):
        """
        reply to certian post
        :param content:content to reply.
        :param tid:id of the post.
        :return:True, or false if post fialed.
        """
        postData = {
            '__type__': 'reply',
            'content': content,
            'fid': self.fid,
            #'floor_num' :   '8',
            'ie': 'utf-8',
            'kw': self.kw,
            'mouse_pwd': MOUSE_CRACK[random.randint(0, len(MOUSE_CRACK)) - 1] + self.timestamp,
            'mouse_pwd_isclick': '0',
            'mouse_pwd_t': self.timestamp,
            'rich_text': '1',
            'tbs': self.tbs,
            'tid': tid,  # id of the post

        }
        reply_req = self.session.post(ADD_REPLY_URL, data=postData)
        # print reply_req.text
        if "\"err_code\":0" in reply_req.text:
            print u'回帖成功!'
            return True
        else:
            print u'回帖失败'
            return False

    def get_repost_id(self, tid, floor_num):
        """
        获取楼中楼回复所需的repostid
        :param tid: id of the post.
        :param floor_num: the num of the floor to reply.
        """
        pn = int(floor_num)/30
        # print pn
        pageUrl = 'http://tieba.baidu.com/p/%s?pn=%d' % (tid, pn)
        page_req = self.session.get(pageUrl)
        pageSoup = BeautifulSoup(page_req.text, 'lxml')
        # with open('test.html','w') as out:
        #     out.write(urllib2.urlopen(pageRequest).read())
        divs = pageSoup.find_all(
            'div', {'class': "l_post j_l_post l_post_bright  "})
        null = None
        false = False
        for div in divs:
            infoDict = eval(div['data-field'])
            if int(floor_num) == infoDict['content']['post_no']:
                return infoDict['content']['post_id']

    def reply_in_floor(self, content, tid, floor_num):
        """
        post reply in floor
        :param content: content to post
        :param tid:id of the whole post
        :param floor_num: floor num
        """
        pid = str(self.get_repost_id(tid, floor_num))
        # print pid
        postData = {
            'ie': 'utf-8',
            'content': content,
            'fid': self.fid,
            'repostid': pid,
            'quote_id': pid,
            'floor_num': floor_num,
            'ie': 'utf-8',
            'kw': self.kw,
            'rich_text': '1',
            'tbs': self.tbs,
            'tid': tid,  # id of the post
            'anonymous': 0

        }
        # print postData

        reply_req = self.session.post(ADD_REPLY_URL, data=postData)
        # print reply_req.text
        if "\"err_code\":0" in reply_req.text:
            print u'回帖成功!'
            return True
        else:
            print u'回帖失败'
            return False

    # 删除回复
    def delete_reply(self, tid, floor_num):
        """
        delete certian reply 
        :param tid:id of the whole post
        :param floor_num: floor num
        """
        pid = str(self.get_repost_id(tid, floor_num))
        postData = {
            'commit_fr': 'pb',
            'fid': self.fid,
            'pid': pid,
            'ie': 'utf-8',
            'kw': self.kw,
            'tbs': self.tbs,
            'tid': tid,  # id of the post
            'is_finf': 'false',
            'is_vipdel': '1',
        }
        delete_req = self.session.post(DELETE_REPLY_URL, data=postData)
        # print delete_req.text
        if "\"err_code\":0" in delete_req.text:
            print u'删除成功!'
            return True
        elif "\"err_code\":220034" in delete_req.text:
            print u'今天删除数目已达上限，请明天再来~'
            return False
        else:
            print u'删除失败'
            return False

    def at_all_user(self, tid):
        f = open('userid.txt', 'r')
        while f.readline():  # once nextline exist
            reply = u''
            count = 0
            while count < 5:  # 回一次贴最多只能艾特5个
                tmp_user = '@' + f.readline().rstrip() + ' '  # add @ and space
                reply += tmp_user  # add to reply content
                count += 1
            # print reply
            result = bar.reply(reply, tid)  # reply in thread
            time.sleep(20)
            while result != True:  # once fail to reply ,sleep for a long time
                time.sleep(60)
                result = bar.reply(reply, tid)

if __name__ == '__main__':
    user = Account(USER_LIST[0]['username'], USER_LIST[0]['password'])
    bar = Bar(FYS_URL, user)
    bar.get_info()
    bar.reply_in_floor('succeed in floor','3974936496','15')
    # for i in range(20, 20):
    #     bar.delete_reply('3974936496', i)
