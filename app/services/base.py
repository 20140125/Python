#!/usr/bin/python3
import json
import time

from app.middleware.checkLogin import MiddlewareMessage
from db.connection import MySQLdb
from tools.logger import logger
from tools.redis import redisClient
from fastapi import Request

ERR_MSG = MiddlewareMessage()


# 保存日志
async def saveLog(params, request: Request):
    try:
        request_params = params['lists']
        username = 'tourist'
        if request.headers.get('Content-Type') == 'application/json':
            request_params = await request.json()
            # 没有登录可以访问的接口获取不到令牌
            if not (request.url.path in ERR_MSG.NOT_LOGIN_ACCESS_URL):
                username = await redisClient.get_value(request_params['token'].upper())
        log = {
            'message': params['message'],
            'request_params': request_params,
            'response_params': params
        }
        return await MySQLdb.update_one(
            'insert into os_system_log (username, url, ip_address, log, created_at, day) values (%s, %s, %s, %s, %s, %s)',
            (
                username,
                request.url,
                request.client.host,
                json.dumps(log, ensure_ascii=True),
                int(time.time()),
                time.strftime("%Y%m%d", time.localtime())
            )
        )
    except Exception as e:
        logger.error('save log error: {}'.format(e))
