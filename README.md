#百度贴吧工具脚本
模拟登陆贴吧进行一系列自动化操作

#使用说明:
##基本操作
>分为account.py和bar.py两个模块，分别处理模拟登陆和模拟操作部分，后者需要前者的登录信息。

###Login 登陆
- 必须要用百度ID登陆，手机号邮箱之类会报错；
- 多次重复登陆需要验证码，抓取到本地文件夹中,从终端输入；
- 异地登录绑定了手机的账号需要短信验证所以登不上，目前还没有解决这个问题，测试困难比较大；
- 第一次登陆后的cookie会以 **用户名+.txt** 格式保存在本地文件夹中,之后默认载入cookie登陆,避免重复登陆招来验证码大法,如果cookie无效才会模拟登陆一次.

>有多个账户时，以以下格式保存在local_settings.py(本地创建)中。

```
USER_LIST=[
    {'username':'','password':''},
    {'username':'','password':''},
}
```

###Post 发帖
需要登陆并且账户已关注该贴吧.
目前无法解决大段文字内容无法分段问题（明明有换行符的情况下）
###Reply 回帖
已楼中楼回复，同一账号短时间回复过多楼层会被判定为刷帖并被抽楼,建议使用time.sleep延时
###Sign 签到
代码大部分参考[skyline75489的github项目](https://github.com/skyline75489/baidu-tieba-auto-sign)

##代码模块说明
###account.py（账号处理部分）
`login_baidu`:登陆函数
`get_bars`:获取关注的贴吧列表
`fetch_tieba_info`:获取单个吧的信息
`sign`:单个贴吧签到
`auto_sign`:遍历关注的吧自动签到
其他为实现功能的工具函数

###bar.py（贴吧处理部分）
`get_info`：获取贴吧信息（用于post数据所带的参数）
`get_user_id`：抓取所有关注者id，保存在文本中
`post`:发帖
`reply`：回帖
`reply_in_floor`:回复楼中楼
`delete_reply`：删除回复（贴吧规定一天只能删除30条自己的回复）
`at_all_user`：一次五个自动艾特全体吧友（易被抽楼）
其他为实现功能的工具函数

###main.py（组合相关函数实现功能）
`up_to_many_post`：自动顶多个不同的贴
`post_article_with_many_paragraphs`：分段自动发布文章
可以根据自己需要组合不同的功能

###snatch.py（抓取其他网站内容的脚本）