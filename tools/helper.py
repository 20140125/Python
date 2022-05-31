#!/usr/bin/python3
import random
from datetime import datetime, timedelta
import jwt

from config.app import Settings
import json
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.middleware.config import MiddlewareMessage
from app.services.v1 import systemLog
from tools.logger import logger

# 错误码信息
code = MiddlewareMessage()
# 获取配置信息
settings = Settings()

"""
todo：返回JSON字符串
Parameter request, message, lists, status of tools.helper.jsonResponse
request: {url, headers, client}
message: str
lists: Any
status: int
return JSONResponse
"""


async def jsonResponse(request, message='successfully', lists=None, status=code.SUCCESS):
    try:
        if lists is None:
            lists = []
        if status == code.ERROR and message == 'successfully':
            message = 'failed'
        data = json.dumps({'message': message, 'code': status, 'lists': lists})
        item = {
            'item': json.loads(data),
            'status_code': 200,
            'url': str(request.url)
        }
        # 保存系统日志到数据库
        await systemLog.save(json.loads(data), request)
        # 返回JSON数据
        return JSONResponse(jsonable_encoder(item))
    except Exception as e:
        logger.info('jsonResponse message： {}'.format(e))


"""
todo： 生成token
Parameter data of tools.helper.create_access_token
data: dict
return str
"""


async def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        # token失效时限
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        # 更新到我们之前传进来的字典
        to_encode.update({'exp': expire})
        # jwt 编码 生成我们需要的token
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.token_algorithm)
        # 返回token信息
        return encoded_jwt
    except Exception as e:
        logger.info('create_access_token message： {}'.format(e))


"""
todo: 设置随机数
Parameter length of tools.helper.set_random_str
length: int
type: str
"""


async def set_random_str(length=6, name='default'):
    try:
        random_str = {
            'number': '0123456789',
            'char': 'QWERTYUIOPLKJHGFDSAZXCVBNMmnbvcxzasdfghjklpoiuytrewq',
            'upper': 'QWERTYUIOPLKJHGFDSAZXCVBNM',
            'lower': 'qwertyuioplkjhgfdsazxcvbnm',
            'default': 'QWERTYUIOPLKJHGFDSAZXCVBNMmnbvcxzasdfghjklpoiuytrewq0123456789'
        }
        string = []
        characters = list(random_str.get(name))
        for i in range(0, length):
            random.shuffle(characters)
            string.append(characters[random.randint(0, len(characters))])
        return ''.join(str(x) for x in string)
    except Exception as e:
        logger.info('set_random_str message： {}'.format(e))
