#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import sqlite3
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 获取所有输注安排数据
conn = sqlite3.connect('doctor_tools.db')
cur = conn.cursor()
cur.execute("select * from infusion_schedule")
schedules = cur.fetchall()

# 企业信息初始化
url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ww39791bfc289e4043&corpsecret=0mr0N20DZ1wZV4B1WpYVlYPd0Q2j70qfjEK6bOArjus"
response = requests.request("GET", url)
access_token = response.json()['access_token']
# access_token = "M3o4d4uuvcvF6ek9ngGjvWbFB4i7cF6G2ss6fjqISYsjnP7Id7kDXj9Y5jeH0SLbsN7l1E5m06ivMjJoLXc9mm9Tk6cPbSYy_rbJc4LjOFDmyWkoFVRUnOgDEIXYWdxUZqjCoF4U16L9b6KYD3LAbYAiWrLk9bttv7T3SaeIpBWvwFM46uPYl-EKtLBKEwCft5DBdJoBFBn0Dg4PvW8jJw"
for schedule in schedules:
    # 如果当前时间介于开始与结束之间，且与开始时间的差值为间隔的整数倍，则发送消息
    print(schedule)
    if True:
        url = "https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token="+access_token

        json = {
            "chatid": "0001",
            "msgtype":"textcard",
            "textcard":{
                "title" : "患者输注通知",
                "description" : "<div class=\"normal\">患者{}将于{}时间进行输注，请合理安排时间哦</div>".format(schedule[1],schedule[2]),
                "url":"https://work.weixin.qq.com/",
                "btntxt":"更多"
            },
            "safe":0
        }
        response = requests.request("POST", url, json=json)
        print(response.text)
