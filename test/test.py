import json
import random

import requests

a = {'code': 20000, 'message': 'get_user_info failed'}

print(a['code'])

print(json.loads('callback( {"error":100068,"error_description":"invalid code, decode fail"} );'.replace('callback', '').replace('(', '').replace(')', '').replace(';', '')))

# verify_code = random.randint(100000, 999999)
#
# config = requests.post('https://www.fanglonger.com/api/v1/oauth/config', {
#     'name': 'oauth'
# })
#
# print(config.json())
#
# mail = requests.post('https://www.fanglonger.com/api/v1/mail/send', {
#     'email': '785973567@qq.com',
#     'verify_code': verify_code
# })
#
# print(mail.json())
#
# login = requests.post('https://www.fanglonger.com/api/v1/account/login', {
#     'email': '785973567@qq.com',
#     'verify_code': verify_code,
#     'loginType': 'email'
# })
#
# print(login.json())
#
