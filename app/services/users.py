#!/usr/bin/python3

import json
import random
from datetime import datetime
from hashlib import md5

from app.middleware.config import MiddlewareMessage
from config.app import Settings
from db.connection import MySQLdb
from tools.redis import redisClient
from tools.token import create_access_token

config = Settings()
Code = MiddlewareMessage()


# 生成验证码
async def verify_code():
    # 生成随机数
    num = random.randint(100000, 999999)
    # 保存到REDIS
    await redisClient.set_ex(num, config.set_redis_timeout, num)
    return {'message': 'successfully', 'code': Code.SUCCESS, 'items': {'verify_code': num}}


# 用户登录系统
async def login(users):
    try:
        # 验证验证码是否正确
        if await redisClient.get_value(users.verify_code) is None:
            return {'message': 'verify code not found', 'code': Code.ERROR}
        # 验证通过删除验证码
        await redisClient.delete_value(users.verify_code)
        # 邮箱验证用户信息
        result = MySQLdb.get_one(
            'select id, username, email, role_id, ip_address, status, created_at, updated_at, password, salt, remember_token, phone_number, avatar_url, uuid, `char` from os_users where email = %s',
            (users.email))
        if result is None:
            return {'message': 'username not found', 'code': Code.NOT_FOUND}
        # 判断用户密码是否正确
        password = md5((md5(users.password.encode('utf-8')).hexdigest() + result['salt']).encode('utf-8')).hexdigest()
        if result['password'] != password:
            return {'message': 'username and password check failed', 'code': Code.ERROR}
        # 保存用户TOKEN数据在Redis
        await redisClient.set_ex(result['remember_token'], config.app_refresh_login_time,
                                 result['remember_token'].upper())
        # 保存用户名
        await redisClient.set_ex(result['remember_token'].upper(), config.app_refresh_login_time, result['username'])
        # 获取角色权限
        role = MySQLdb.get_one('select auth_api from os_role where id = %s', (result['role_id']))
        result['auth_api'] = json.loads(role['auth_api'])
        return {'message': 'successfully', 'code': Code.SUCCESS, 'lists': result}
    except Exception as e:
        return {'message': 'network error {}'.format(e), 'code': Code.NETWORK}


# 登出系统
async def logout(users):
    try:
        result = MySQLdb.get_one('select id, role_id, remember_token from os_users where remember_token = %s',
                                 (users.remember_token))
        if result is None:
            return {'message': 'failed', 'code': Code.ERROR}
        # 删除保存在Redis的用户TOKEN数据
        await redisClient.delete_value(users.remember_token)
        token = create_access_token({'remember_token': result['username'] + str(datetime.utcnow())})
        result['remember_token'] = token
        # 更新用户表TOKEN
        return {'message': 'successfully', 'code': Code.SUCCESS, 'lists': result}
    except Exception as e:
        return {'message': 'network error {}'.format(e), 'code': Code.NETWORK}


async def register(users):
    return {'code': Code.ERROR, 'users': users}
