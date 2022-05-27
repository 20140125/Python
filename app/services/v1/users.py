#!/usr/bin/python3

import json
import random
from datetime import datetime
from hashlib import md5
from secrets import compare_digest

import db.models as models
import tools.helper as helper
from app.middleware.config import MiddlewareMessage
from config.app import Settings
from db.crud.role import get_one_role
import db.crud.users as users_orm
from tools.redis import redisClient
from tools.token import create_access_token

config = Settings()
Code = MiddlewareMessage()


# 用户登录系统
async def login(params, request):
    try:
        # 验证验证码是否正确
        if await redisClient.get_value(params.captcha) is None:
            return await helper.jsonResponse(
                await helper.return_params(message='verify code not found', code=Code.ERROR),
                request)
        # 邮箱验证用户信息
        result = users_orm.get_one_user([models.Users.email == params.email])
        if result is None:
            return await helper.jsonResponse(
                await helper.return_params(message='username not found', code=Code.NOT_FOUND),
                request)
        # 判断用户密码是否正确
        password = md5(
            (md5(params.password.encode('utf-8')).hexdigest() + result['salt']).encode('utf-8')).hexdigest()
        if compare_digest(result['password'], password):
            return await helper.jsonResponse(
                await helper.return_params(message='username and password check failed', code=Code.ERROR), request)
        # 保存用户TOKEN数据在Redis
        await redisClient.set_ex(result['remember_token'], config.app_refresh_login_time,
                                 result['remember_token'].upper())
        # 保存用户名
        await redisClient.set_ex(result['remember_token'].upper(), config.app_refresh_login_time,
                                 result['username'])
        # 获取角色权限
        item = get_one_role([models.Role.id == result['role_id']])
        result['auth_api'] = json.loads(item['auth_api'])
        # 验证通过删除验证码
        await redisClient.delete_value(params.captcha)
        # 返回数据
        return await helper.jsonResponse(await helper.return_params(lists=result), request)
    except Exception as e:
        return await helper.jsonResponse(
            await helper.return_params(message='network error {}'.format(e), code=Code.NETWORK),
            request)


# 获取用户列表
async def lists(params, request):
    try:
        result = users_orm.get_user_lists(page=params.page, limit=params.limit)
        return await helper.jsonResponse(await helper.return_params(lists=result), request)
    except Exception as e:
        return await helper.jsonResponse(
            await helper.return_params(message='network error {}'.format(e), code=Code.NETWORK), request)


# 登出系统
async def logout(params, request):
    try:
        result = users_orm.get_one_user([compare_digest(models.Users.remember_token, params.token)])
        if result is None:
            return await helper.jsonResponse(await helper.return_params(code=Code.ERROR), request)
        # 删除保存在Redis的用户TOKEN数据
        await redisClient.delete_value(params.token)
        token = await create_access_token({'authentication': result['username'] + str(datetime.utcnow())})
        result['remember_token'] = token
        # 更新用户表TOKEN
        return await helper.jsonResponse(await helper.return_params(lists=result), request)
    except Exception as e:
        return await helper.jsonResponse(
            await helper.return_params(message='network error {}'.format(e), code=Code.NETWORK),
            request)


# 注册用户
async def register(params, request):
    result = users_orm.get_one_user([models.Users.email == 'loveqin0125@foxmail.com'])
    return await helper.jsonResponse(await helper.return_params(lists=result), request)
