#!/usr/bin/python3

import json
import time

from db import models
from db.crud import systemLog
from tools import helper
from tools.logger import logger
from tools.redis import redisClient


async def lists(pagination, request):
    """
    todo：获取日志列表
    :param pagination:
    :param request:
    :return JSONResponse:
    """
    try:
        result = systemLog.lists(page=pagination.page, limit=pagination.limit)
        if result['items'] is not None:
            for item in result['items']:
                if await helper.is_json_string(item['log']):
                    item['log'] = json.loads(item['log'])
        return await helper.jsonResponse(request, lists=result)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


async def remove(params, request):
    """
    todo：删除日志
    :param params:
    :param request:
    :return JSONResponse:
    """
    try:
        if systemLog.delete([models.Log.id == params.id]):
            return await helper.jsonResponse(request, lists={'id': params.id})
        return await helper.jsonResponse(request, lists={'id': params.id}, status=helper.code.ERROR)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


async def save(params, request):
    """
    todo：保存日志
    :param params:
    :param request:
    :return:
    """
    try:
        request_params = params['lists']
        username = 'tourist'
        if request.headers.get('Content-Type') == 'application/json':
            request_params = await request.json()
            # 没有登录可以访问的接口获取不到令牌
            if not (request.url.path in helper.code.NOT_LOGIN_ACCESS_URL):
                username = await redisClient.get_value(request_params['token'].upper())
        log = models.Log(
            username=username,
            url=request.url,
            ip_address=request.client.host,
            log=json.dumps({
                'message': params['message'],
                'request_params': request_params,
                'response_params': params['lists']
            }, ensure_ascii=True),
            created_at=int(time.time()),
            day=time.strftime("%Y%m%d", time.localtime())
        )
        return systemLog.save(log)
    except Exception as e:
        logger.error('save log error: {}'.format(e))
