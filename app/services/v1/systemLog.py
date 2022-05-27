#!/usr/bin/python3

from db.crud import systemLog
import json
import time

from tools import helper
from tools.logger import logger
from tools.redis import redisClient


# 获取日志列表
async def lists(pagination, request):
    try:
        result = systemLog.lists(page=pagination.page, limit=pagination.limit)
        if result['items'] is not None:
            for item in result['items']:
                item['log'] = json.loads(item['log'])
        return await helper.jsonResponse(request, lists=result)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


# 删除日志
async def remove(params, request):
    try:
        count = systemLog.delete(params)
        if count > 0:
            return await helper.jsonResponse(request, lists=params, message='remove system log successfully')
        return await helper.jsonResponse(request, lists=params, message='remove system log failed', status=helper.code.ERROR)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


# 保存日志
async def save(params, request):
    try:
        request_params = params['lists']
        username = 'tourist'
        if request.headers.get('Content-Type') == 'application/json':
            request_params = await request.json()
            # 没有登录可以访问的接口获取不到令牌
            if not (request.url.path in helper.code.NOT_LOGIN_ACCESS_URL):
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
        return systemLog.save(log)
    except Exception as e:
        logger.error('save log error: {}'.format(e))

