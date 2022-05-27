#!/usr/bin/python3
import json
import time
import random

from fastapi import Request

from app.middleware.config import MiddlewareMessage
from db.crud.systemLog import insert_log
from config.app import Settings
from tools import helper
from tools.logger import logger
from tools.redis import redisClient

ERR_MSG = MiddlewareMessage()

config = Settings()


# 保存日志
async def save_log(params, request: Request):
    try:
        request_params = params['lists']
        username = 'tourist'
        if request.headers.get('Content-Type') == 'application/json':
            request_params = await request.json()
            # 没有登录可以访问的接口获取不到令牌
            if not (request.url.path in ERR_MSG.NOT_LOGIN_ACCESS_URL):
                username = await redisClient.get_value(request_params['token'].upper())
        log = {
            'username': username,
            'url': request.url,
            'ip_address': request.client.host,
            'log': json.dumps({
                'message': params['message'],
                'request_params': request_params,
                'response_params': params
            }, ensure_ascii=True),
            'created_at': int(time.time()),
            'day': time.strftime("%Y%m%d", time.localtime())
        }
        return insert_log(log)
    except Exception as e:
        logger.error('save log error: {}'.format(e))


# 生成验证码
async def captcha(request):
    # 生成随机数
    num = random.randint(100000, 999999)
    # 保存到REDIS
    await redisClient.set_ex(num, config.set_redis_timeout, num)
    return await helper.jsonResponse(await helper.return_params(lists={'captcha': num}), request)
