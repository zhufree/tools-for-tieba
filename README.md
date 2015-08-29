# tools-for-tieba
some codes to help to do something in baidutieba
##模拟登陆贴吧与操作
###Login 登陆
必须要用百度ID登陆，手机号邮箱之类会报错，验证码暂时无解,异地登录绑定了手机的账号需要短信验证所以登不上
###Post 发帖
目前无法解决大段文字内容无法分段问题（明明有换行符的情况下）
###Reply 回帖
不支持楼中楼回复，同一账号回复过多楼层会被判定为刷帖并被抽楼
###Sign 签到
代码大部分参考[skyline75489的github项目](https://github.com/skyline75489/baidu-tieba-auto-sign)

##snatch 抓取
### get\_from_wechat函数
用于抓取微信公众号的文章，一些用秀米排版的文章文字抓取不全

其余的网站慢慢加

