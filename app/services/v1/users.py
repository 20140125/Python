#!/usr/bin/python3

import json
from datetime import datetime
from hashlib import md5
from secrets import compare_digest

from db import models
from tools import helper
from db.crud import role, users
from tools.redis import redisClient


# 用户登录系统
async def login(params, request):
    try:
        # 验证验证码是否正确
        if await redisClient.get_value(params.captcha) is None:
            return await helper.jsonResponse(request, message='verify code not found', status=helper.code.ERROR)
        # 邮箱验证用户信息
        result = users.get([models.Users.email == params.email])
        if result is None:
            return await helper.jsonResponse(request, message='username not found', status=helper.code.NOT_FOUND)
        # 判断用户密码是否正确
        password = md5(
            (md5(params.password.encode('utf-8')).hexdigest() + result['salt']).encode('utf-8')).hexdigest()
        if compare_digest(result['password'], password):
            return await helper.jsonResponse(request, message='username and password check failed',
                                             status=helper.code.ERROR)
        # 保存用户TOKEN数据在Redis
        await redisClient.set_ex(result['remember_token'], helper.settings.app_refresh_login_time,
                                 result['remember_token'].upper())
        # 保存用户名
        await redisClient.set_ex(result['remember_token'].upper(), helper.settings.app_refresh_login_time,
                                 result['username'])
        # 获取角色权限
        item = role.get([models.Role.id == result['role_id']])
        result['auth_api'] = json.loads(item['auth_api'])
        # 验证通过删除验证码
        await redisClient.delete_value(params.captcha)
        # 返回数据
        return await helper.jsonResponse(request, lists=result)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


# 获取用户列表
async def lists(params, request):
    try:
        result = users.lists(page=params.page, limit=params.limit)
        return await helper.jsonResponse(request, lists=result)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


# 登出系统
async def logout(params, request):
    try:
        result = users.get([models.Users.remember_token == params.token])
        if result is None:
            return await helper.jsonResponse(request, status=helper.code.ERROR)
        # 删除保存在Redis的用户TOKEN数据
        await redisClient.delete_value(params.token)
        token = await helper.create_access_token({'authentication': '{}{}'.format(str(result['username']), str(datetime.utcnow()))})
        result['remember_token'] = token
        # 更新用户表TOKEN
        return await helper.jsonResponse(request, lists=result)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


# 注册用户
async def register(params, request):
    result = users.get([models.Users.email == 'loveqin0125@foxmail.com'])
    print(result['username'])
    return await helper.jsonResponse(request, lists=result)
