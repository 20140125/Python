#!/usr/bin/python3

import json
import random
import time
from hashlib import md5
from secrets import compare_digest

from db import models
from db.crud import role, users
from tools import helper
from tools.logger import logger
from tools.redis import redisClient

"""
todo：用户登录系统
Parameter params, request of app.services.v1.users.login 
params: {captcha, email, password}
request: {url, headers, client}
return JSONResponse
"""


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
            return await helper.jsonResponse(
                request,
                message='username and password check failed',
                status=helper.code.ERROR
            )
        # 保存用户TOKEN数据在Redis
        await redisClient.set_ex(
            result['remember_token'],
            helper.settings.app_refresh_login_time,
            result['remember_token'].upper()
        )
        # 保存用户名
        await redisClient.set_ex(
            result['remember_token'].upper(),
            helper.settings.app_refresh_login_time,
            result['username']
        )
        # 获取角色权限
        item = role.get([models.Role.id == result['role_id']])
        result['auth_api'] = json.loads(item['auth_api'])
        # 验证通过删除验证码
        await redisClient.delete_value(params.captcha)
        # 返回数据
        return await helper.jsonResponse(request, lists=result)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


"""
todo：获取用户列表
Parameter params, request of app.services.v1.users.logout
params: {page, limit}
request: {url, headers, client}
return JSONResponse
"""


async def lists(params, request):
    try:
        result = users.lists(page=params.page, limit=params.limit)
        return await helper.jsonResponse(request, lists=result)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


"""
todo：登出系统
Parameter params, request of app.services.v1.users.logout
params: {token}
request: {url, headers, client}
return JSONResponse
"""


async def logout(params, request):
    try:
        result = users.get([models.Users.remember_token == params.token])
        if result is None:
            return await helper.jsonResponse(request, status=helper.code.ERROR)
        # 删除保存在Redis的用户TOKEN数据
        await redisClient.delete_value(params.token)
        return await helper.jsonResponse(request, lists=result)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


"""
todo: 注册用户
Parameter params, request of app.services.v1.users.register
params: {email, captcha}
request: {url, headers, client}
return JSONResponse
"""


async def register(params, request):
    try:
        # 验证验证码是否正确
        if await redisClient.get_value(params.captcha) is None:
            return await helper.jsonResponse(request, message='verify code not found', status=helper.code.ERROR)
        salt = await helper.set_random_str()
        token = await helper.create_access_token({'authentication': '{}{}'.format(params.email, str(time.time()))})
        password = md5((md5(helper.settings.default_password.encode('utf-8')).hexdigest() + salt).encode('utf-8')).hexdigest()
        user = models.Users(
            avatar_url=await get_avatar_url(),
            salt=salt,
            email=params.email,
            password=password,
            role_id=2,
            status=1,
            ip_address=request.client.host,
            created_at=int(time.time()),
            updated_at=int(time.time()),
            remember_token=token,
            uuid=helper.settings.default_uuid,
            phone_number=''
        )
        user_id = users.save(user)
        if user_id is None:
            return await helper.jsonResponse(request, status=helper.code.ERROR)
        if users.update({'id': user_id, 'uuid': helper.settings.default_uuid}):
            # 保存用户个人中心信息
            return await helper.jsonResponse(request, lists=({'id': user_id}))
        return await helper.jsonResponse(request, status=helper.code.ERROR)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


"""
todo: 获取随机用户图片
return Optional[Any]
"""


async def get_avatar_url():
    try:
        cache_user = await get_cache_users()
        cache = []
        for k in cache_user:
            if k['username'] != 'admin':
                cache.append(k['avatar_url'])
        return cache[random.randint(0, len(cache))]
    except Exception as e:
        logger.error('get_avatar_url error message: {}'.format(e))
        return None


"""
todo: 获取缓存用户信息
return Optional[Any]
"""


async def get_cache_users():
    try:
        user = await redisClient.s_members(helper.settings.users_cache_key)
        cache_user = None
        for i in user:
            cache_user = json.loads(i)
        return cache_user
    except Exception as e:
        logger.error('get_cache_users error message: {}'.format(e))
        return None


"""
todo: 设置缓存用户信息
return None
"""


async def set_cache_users():
    try:
        user = users.all_users()
        await redisClient.s_add(helper.settings.users_cache_key, json.dumps(user, ensure_ascii=True))
    except Exception as e:
        logger.error('set_cache_users error message: {}'.format(e))
        return None
