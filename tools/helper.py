#!/usr/bin/python3
import json

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.middleware.config import MiddlewareMessage
from app.services import common
from tools.logger import logger

Code = MiddlewareMessage()


# 设置返回的数据格式
async def return_params(message='successfully', lists=None, code=Code.SUCCESS):
    if lists is None:
        lists = []
    if code == Code.ERROR and message == 'successfully':
        message = 'failed'
    return json.dumps({'message': message, 'code': code, 'lists': lists})


# 返回JSON字符串
async def jsonResponse(data, request: Request, code: int = 200):
    try:
        item = {
            'item': json.loads(data),
            'status_code': code,
            'url': str(request.url)
        }
        # 保存系统日志到数据库
        await common.save_log(json.loads(data), request)
        # 返回JSON数据
        return JSONResponse(jsonable_encoder(item))
    except Exception as e:
        logger.info('error message： {}'.format(e))
