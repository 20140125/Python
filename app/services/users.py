#!/usr/bin/python3

import json
import random
from datetime import datetime
from hashlib import md5

from app.middleware.config import MiddlewareMessage
from config.app import Settings
from db.crud.role import get_one_role
from db.crud.users import get_one_user
from db.orm.role import Role
from db.orm.users import Users
from tools.helper import (jsonResponse, return_params)
from tools.redis import redisClient
from tools.token import create_access_token

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
        if await redisClient.get_value(users.captcha) is None:
            return await jsonResponse(await return_params(message='verify code not found', code=Code.ERROR), request)
        # 邮箱验证用户信息
        result = get_one_user([Users.email == users.email])
        if result is None:
            return await jsonResponse(await return_params(message='username not found', code=Code.NOT_FOUND), request)
        # 判断用户密码是否正确
        password = md5((md5(users.password.encode('utf-8')).hexdigest() + result['salt']).encode('utf-8')).hexdigest()
        if result['password'] != password:
            return await jsonResponse(
                await return_params(message='username and password check failed', code=Code.ERROR), request)
        # 保存用户TOKEN数据在Redis
        await redisClient.set_ex(result['remember_token'], config.app_refresh_login_time,
                                 result['remember_token'].upper())
        # 保存用户名
        await redisClient.set_ex(result['remember_token'].upper(), config.app_refresh_login_time, result['username'])
        # 获取角色权限
        role = get_one_role([Role.id == result['role_id']])
        result['auth_api'] = json.loads(role['auth_api'])
        # 验证通过删除验证码
        await redisClient.delete_value(users.captcha)
        # 返回数据
        return await jsonResponse(await return_params(lists=result), request)
    except Exception as e:
        return await jsonResponse(await return_params(message='network error {}'.format(e), code=Code.NETWORK), request)


# 登出系统
async def logout(users, request):
    try:
        result = get_one_user([Users.remember_token == users.token])
        if result is None:
            return await jsonResponse(await return_params(code=Code.ERROR), request)
        # 删除保存在Redis的用户TOKEN数据
        await redisClient.delete_value(users.token)
        token = await create_access_token({'authentication': result['username'] + str(datetime.utcnow())})
        result['remember_token'] = token
        # 更新用户表TOKEN
        return await jsonResponse(await return_params(lists=result), request)
    except Exception as e:
        return await jsonResponse(await return_params(message='network error {}'.format(e), code=Code.NETWORK), request)


# 注册用户
async def register(users, request):
    result = get_one_user([Users.username == 'admin'])
    return await jsonResponse(await return_params(lists=result), request)
