#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from flask import Flask,request
from wework_lib.WXBizMsgCrypt import WXBizMsgCrypt
import re
import sqlite3

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def receive_msg():
    sToken = "Kt2SCl5n"
    sEncodingAESKey = "RQGhS9c3OtfdtYpd6Sk9hyQqXeap9y7HexmKMMFWV2y"
    sCorpID = "ww39791bfc289e4043"
    wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)

    if request.method == "GET":
        ret, sEchoStr = wxcpt.VerifyURL(request.args["msg_signature"], request.args["timestamp"], request.args["nonce"], request.args["echostr"])
        if ret == 0:
            return sEchoStr
        else:
            return "unauth"
    elif request.method == "POST":
        ret, sMsg = wxcpt.DecryptMsg(request.data, request.args["msg_signature"], request.args["timestamp"], request.args["nonce"])
        print sMsg

        # 提取用户发送消息
        uMsg = re.search(r'<Content>([\s\S]*)</Content>', sMsg).group().replace("<Content><![CDATA[","").replace("]]></Content>","")
        if uMsg !=None:
            data = {
                "name":"贾一飞",
                "start_time":"2021-01-01",
                "end_time":"2022-01-01",
                "interval":7
            }
            for field in uMsg.split("\n"):
                key = field.split(":")[0]
                value = field.split(":")[1]
                if key == "患者":
                    data["name"] = value
                elif key == "开始时间":
                    data["start_time"] = value
                elif key == "结束时间":
                    data["end_time"] = value
                elif key == "时间间隔":
                    data["interval"] = value

            # 提醒信息入库
            conn = sqlite3.connect('doctor_tools.db')
            c = conn.cursor()
            c.execute("select * from infusion_schedule order by id desc")
            schedule = c.fetchone()

            c.execute(
                "INSERT INTO 'infusion_schedule' VALUES ({},\"{}\",\"{}\",\"{}\",{})".format(schedule[0]+1,data["name"],data["start_time"],data["end_time"],data["interval"])
            )
            conn.commit()
            conn.close()

        if ret == 0:
            print ret, sMsg
            return "success"
        else:
            return "unauth"

@app.route("/test")
def test():
    return "hello"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)