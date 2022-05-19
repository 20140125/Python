#!/usr/bin/python3

from db.connection import MySQLdb

from hashlib import md5

from tools.token import create_access_token

from datetime import datetime
import random

#生成验证码
async def set_verify_code():
    return {'message': 'successfully', 'code': 200, 'items': {'verify_code': random.randint(100000, 999999)}}

# 用户登录系统
async def login(users):
    try:
        result = MySQLdb.get_one('select * from os_users where email = %s', (users.email,))
        if result is not None:
            if result['password'] == md5((md5(users.password.encode('utf-8')).hexdigest() + result['salt']).encode('utf-8')).hexdigest():
                info = {'message': 'successfully', 'code': 20000, 'items': result}
            else:
                info = {'message': 'username and password check failed', 'code': 20001}
        else:
            info = {'message': 'username not found', 'code': 20001}
    except Exception as e:
        info = {'message': 'network error {}'.format(e), 'code': 50000}
    return info


# 登出系统
async def logout(users):
    try:
        result = MySQLdb.get_one('select * from os_users where remember_token = %s', (users.remember_token,))
        if result is not None:
            token = create_access_token({'remember_token': result['username'] + str(datetime.utcnow())})
            result['remember_token'] = token
            info = {'message': 'successfully', 'code': 20000, 'items': result}
        else:
            info = {'message': 'failed', 'code': 20001}
    except Exception as e:
        print(e)
        info = {'message': 'network error {}'.format(e), 'code': 50000}
    return info


async def register(users):
   return {'code': 20001, 'users': users}