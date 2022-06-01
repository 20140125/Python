#!/usr/bin/python3

import json
import random
import time
from hashlib import md5
from secrets import compare_digest

from db import models
from db.crud import role, users, userCenter
from tools import helper
from tools.logger import logger
from tools.redis import redisClient
from pypinyin import lazy_pinyin, Style

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
        await save_remember_token_to_redis(result['remember_token'], result['remember_token'].upper())
        # 保存用户名
        await save_remember_token_to_redis(result['remember_token'].upper(), result['username'])
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
Parameter pagination, request of app.services.v1.users.logout
pagination: {page, limit}
request: {url, headers, client}
return JSONResponse
"""


async def lists(pagination, request):
    try:
        result = users.lists(page=pagination.page, limit=pagination.limit)
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
        # 如果用户存在直接放回用户信息且更新用户信息
        salt = await helper.set_random_str(length=8)
        token = await helper.create_access_token({'authentication': '{}{}'.format(params.email, str(time.time()))})
        password = md5(
            (md5(helper.settings.default_password.encode('utf-8')).hexdigest() + salt).encode('utf-8')).hexdigest()
        user = users.get([models.Users.email == params.email])
        if user is not None:
            user['salt'] = salt
            user['remember_token'] = token
            user['password'] = password
            users.update(models.Users(
                updated_at=int(time.time()),
                salt=user['salt'],
                password=user['password'],
                remember_token=user['remember_token'],
                ip_address=request.client.host,
                char=lazy_pinyin(await helper.get_random_name(), style=Style.FIRST_LETTER)[0].upper()
            ), [models.Users.id == user['id']])
            # 验证通过删除验证码
            await redisClient.delete_value(params.captcha)
            # 保存用户个人中心信息
            userCenter.update(models.UsersCenter(token=user['remember_token']), [models.UsersCenter.uid == user['id']])
            # 保存用户TOKEN数据在Redis
            await save_remember_token_to_redis(user['remember_token'], user['remember_token'].upper())
            # 保存用户名
            await save_remember_token_to_redis(user['remember_token'].upper(), user['username'])
            return await helper.jsonResponse(request, lists=user)
        # 注册用户信息
        username = await helper.get_random_name()
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
            phone_number='',
            username=username,
            char=lazy_pinyin(username, style=Style.FIRST_LETTER)[0].upper()
        )
        user_id = users.save(user)
        if user_id is None:
            return await helper.jsonResponse(request, status=helper.code.ERROR)
        # 保存用户个人中心信息
        userCenter.save(models.UsersCenter(uid=user_id, token=user.remember_token, u_name=user.username))
        # 更新用户图像
        await set_cache_users()
        # 验证通过删除验证码
        await redisClient.delete_value(params.captcha)
        # 保存用户TOKEN数据在Redis
        await save_remember_token_to_redis(token, token.upper())
        # 保存用户名
        await save_remember_token_to_redis(token.upper(), username)
        # 判断用户信息是否更新成功
        if users.update(models.Users(uuid=helper.settings.default_uuid), [models.Users.id == user_id]):
            return await helper.jsonResponse(request, lists=models.to_json(user))
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
            if k['client_name'] != 'admin':
                cache.append(k['client_img'])
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
        cache_user = []
        for user in users.all_users():
            cache_user.append({
                'client_name': user['username'],
                'client_img': user['avatar_url'],
                'uuid': user['uuid'],
                'id': user['id'],
                'char': user['char'],
                'center': userCenter.get([models.UsersCenter.uid == user['id']])
            })
        await redisClient.s_add(helper.settings.users_cache_key, json.dumps(cache_user, ensure_ascii=True))
    except Exception as e:
        logger.error('set_cache_users error message: {}'.format(e))
        return None


# 保存数据至Redis
async def save_remember_token_to_redis(key, value):
    # 保存用户名
    await redisClient.set_ex(key, helper.settings.app_refresh_login_time, value)
