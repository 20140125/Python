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
from tools.helper import (jsonResponse, return_params)

config = Settings()
Code = MiddlewareMessage()


# 生成验证码
async def captcha(request):
    # 生成随机数
    num = random.randint(100000, 999999)
    # 保存到REDIS
    await redisClient.set_ex(num, config.set_redis_timeout, num)
    return await jsonResponse(await return_params(lists={'captcha': num}), request)


# 用户登录系统
async def login(users, request):
    try:
        # 验证验证码是否正确
        if await redisClient.get_value(users.verify_code) is None:
            return await jsonResponse(await return_params(message='verify code not found', code=Code.ERROR), request)
        # 验证通过删除验证码
        await redisClient.delete_value(users.verify_code)
        # 邮箱验证用户信息
        result = MySQLdb.get_one(
            'select id, username, email, role_id, ip_address, status, created_at, updated_at, password, salt, remember_token, phone_number, avatar_url, uuid, `char` from os_users where email = %s',
            (users.email))
        if result is None:
            return await jsonResponse(await return_params(message='username not found', code=Code.NOT_FOUND), request)
        # 判断用户密码是否正确
        password = md5((md5(users.password.encode('utf-8')).hexdigest() + result['salt']).encode('utf-8')).hexdigest()
        if result['password'] != password:
            return await jsonResponse(await return_params(message='username and password check failed', code=Code.ERROR), request)
        # 保存用户TOKEN数据在Redis
        await redisClient.set_ex(result['remember_token'], config.app_refresh_login_time, result['remember_token'].upper())
        # 保存用户名
        await redisClient.set_ex(result['remember_token'].upper(), config.app_refresh_login_time, result['username'])
        # 获取角色权限
        role = MySQLdb.get_one('select auth_api from os_role where id = %s', (result['role_id']))
        result['auth_api'] = json.loads(role['auth_api'])
        return await jsonResponse(await return_params(lists=result),request)
    except Exception as e:
        return await jsonResponse(await return_params(message='network error {}'.format(e), code=Code.NETWORK), request)

# 登出系统
async def logout(users, request):
    try:
        result = MySQLdb.get_one('select id, role_id, remember_token from os_users where remember_token = %s',
                                 (users.remember_token))
        if result is None:
            return await jsonResponse(await return_params(code=Code.ERROR),request)
        # 删除保存在Redis的用户TOKEN数据
        await redisClient.delete_value(users.remember_token)
        token = await create_access_token({'remember_token': result['username'] + str(datetime.utcnow())})
        result['remember_token'] = token
        # 更新用户表TOKEN
        return await jsonResponse(await return_params(lists=result),request)
    except Exception as e:
        return await jsonResponse(await return_params(message='network error {}'.format(e), code=Code.NETWORK), request)

# 注册用户
async def register(users, request):
    return await jsonResponse(await return_params(lists=users),request)
