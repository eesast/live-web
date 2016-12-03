# -*- coding:utf-8 -*-
from requests import post
import urllib
import json



url = 'http://183.172.234.84:8000/login'
data = {'name':'昊哥', 'msg':'DcJe','img':'http://wx.qlogo.cn/mmopen/ibXAvibKoDicQQKicdkksaXeRJFwLEia0u10J5p4X0iasCqpV26vfd65xpCVd3uLeQrVVQHYbLmL9ZEt2TEAjhRibTkVRB5VW4agKeo/0'}
headers = {'Content-Type': 'application/json'}
response=post(url=url, headers=headers, data=json.dumps(data))

print (response.text)



