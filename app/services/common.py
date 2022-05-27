#!/usr/bin/python3
import random

from app.middleware.config import MiddlewareMessage
from config.app import Settings
from tools import helper
from tools.redis import redisClient

ERR_MSG = MiddlewareMessage()

config = Settings()


# 生成验证码
async def captcha(request):
    # 生成随机数
    num = random.randint(100000, 999999)
    # 保存到REDIS
    await redisClient.set_ex(num, config.set_redis_timeout, num)
    return await helper.jsonResponse(lists={'captcha': num}, request=request)
