#!/usr/bin/python3
import random
from tools import helper


"""
todo：生成验证码
Parameter request of app.services.common.captcha
request: {url, headers, client}
return JSONResponse
"""


async def captcha(request):
    # 生成随机数
    num = random.randint(100000, 999999)
    # 保存到REDIS
    await helper.save_remember_token_to_redis(num, num, helper.settings.set_redis_timeout)
    return await helper.jsonResponse(request, lists={'captcha': num})
