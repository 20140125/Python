#!/usr/bin/python3


import json
from hashlib import md5

import flask
from flask import request

from MysqlConnection import MySQLdb

"""
flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
登录接口，需要传url、username、passwd
"""

# 创建一个服务
server = flask.Flask(__name__)
# 数据库链接
MySQLdb = MySQLdb('localhost', 'root', '123456789', 'longer')


@server.route('/login', methods=['get', 'post'])
def login():
    username = request.values.get('username')
    password = request.values.get('password')
    if username and password:
        res = get_user(username, password)
    else:
        res = {'message': 'username and password are required', 'code': 201}
    return json.dumps(res, ensure_ascii=True)


def get_user(username, password):
    try:
        res = MySQLdb.get_one("SELECT * FROM os_users WHERE username = %s", (username,))
        if res['password'] == md5((md5(password.encode('utf-8')).hexdigest() + res['salt']).encode('utf-8')).hexdigest():
            info = {'message': 'password check successfully', 'code': 200, 'item': res}
        else:
            info = {'message': 'password check failed', 'code': 201}
    except Exception as e:
        info = {'message': e, 'code': 500}
    return info


if __name__ == '__main__':
    server.run(port=8888, debug=True, host='127.0.0.1')
