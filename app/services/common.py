#!/usr/bin/python3
import random
from tools import helper
from db.crud import users
from db import models


async def captcha(request):
    """
    todo：生成验证码
    :param request:
    :return JSONResponse:
    """
    # 生成随机数
    num = random.randint(100000, 999999)
    # 保存到REDIS
    await helper.save_remember_token_to_redis(num, num, helper.settings.set_redis_timeout)
    return await helper.jsonResponse(request, lists={'captcha': num})


async def set_token(params, request):
    """
       todo：保存用户TOKEN数据在Redis
       :param params:
       :param request:
       :return JSONResponse:
       """
    try:
        result = users.get([models.Users.remember_token == params.token])
        if result is None:
            return await helper.jsonResponse(request, status=helper.code.ERROR)
        # 保存用户TOKEN数据在Redis
        await helper.save_remember_token_to_redis(params.token, params.token.upper())
        # 保存用户名
        await helper.save_remember_token_to_redis(params.token.upper(), result['username'])
        return await helper.jsonResponse(request, lists=result)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)
