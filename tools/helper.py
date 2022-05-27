#!/usr/bin/python3
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


# 返回JSON字符串
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
        logger.info('error message： {}'.format(e))


# 生成token
async def create_access_token(data: dict):
    to_encode = data.copy()
    # token失效时限
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    # 更新到我们之前传进来的字典
    to_encode.update({'exp': expire})
    # jwt 编码 生成我们需要的token
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.token_algorithm)
    # 返回token信息
    return encoded_jwt
