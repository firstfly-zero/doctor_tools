#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import sqlite3
import requests
import sys
import datetime
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
for schedule in schedules:
    # 如果当前时间介于开始与结束之间，且与开始时间的差值为间隔的整数倍，则发送消息
    print(schedule)
    try:
        if str(datetime.date.today()) > schedule[2] and str(datetime.date.today()) < schedule[3] and (datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d') - datetime.datetime.strptime(schedule[2], '%Y-%m-%d') ).days % schedule[4] == 0:
            url = "https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token=" + access_token

            json = {
                "touser": schedule[5],
                "msgtype": "text",
                "agentid": 1000009,
                "text": {
                    "content": "患者{}明天要进行药物输注，请合理安排时间哦".format(schedule[1])
                },
                "safe": 0,
                "enable_id_trans": 0,
                "enable_duplicate_check": 0,
                "duplicate_check_interval": 1800
            }
            response = requests.request("POST",
                                        "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + access_token,
                                        json=json)
            print(response.text)
    except:
        continue
