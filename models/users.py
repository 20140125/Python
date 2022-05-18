#!/usr/bin/python3

from db.connection import MySQLdb

from hashlib import md5

from tools.token import create_access_token

from datetime import datetime


# 用户登录系统
async def login(username, password):
    try:
        result = MySQLdb.get_one('select * from os_users where username = %s', (username,))
        if result['password'] == md5(
                (md5(password.encode('utf-8')).hexdigest() + result['salt']).encode('utf-8')).hexdigest():
            info = {'message': 'successfully', 'code': 20000, 'items': result}
        else:
            info = {'message': 'username and password check failed', 'code': 20001}
    except Exception as e:
        info = {'message': 'network error {}'.format(e), 'code': 50000}
    return info


# 登出系统
async def logout(remember_token):
    try:
        result = MySQLdb.get_one('select * from os_users where remember_token = %s', (remember_token,))
        if result is not None:
            token = create_access_token({'remember_token': result['username'] + str(datetime.utcnow())})
            result['remember_token'] = token
        else:
            result = {
                'remember_token':  create_access_token({'remember_token': 'remember_token' + str(datetime.utcnow())}),
                'type': 'bearer'
            }
        info = {'message': 'successfully', 'code': 20000, 'items': result}
    except Exception as e:
        print(e)
        info = {'message': 'network error {}'.format(e), 'code': 50000}
    return info
