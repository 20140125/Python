#!/usr/bin/python3
import json

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.services.base import saveLog
from tools.logger import logger


# 返回JSON字符串
async def jsonResponse(data: dict, request: Request, code: int = 200):
    try:
        item = {
            'item': data,
            'code': code,
            'url': str(request.url)
        }
        await saveLog(data, request)
        return JSONResponse(jsonable_encoder(item))
    except Exception as e:
        logger.info('error message： {}'.format(e))
