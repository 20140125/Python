#!/usr/bin/python3
import json

from app.middleware.config import MiddlewareMessage
from tools.helper import jsonResponse, return_params
from db.crud.systemLog import get_log_lists, delete_log

Code = MiddlewareMessage()


# 获取日志列表
async def lists(pagination, request):
    try:
        result = get_log_lists(page=pagination.page, limit=pagination.limit)
        if result['items'] is not None:
            for item in result['items']:
                item['log'] = json.loads(item['log'])
        return await jsonResponse(await return_params(lists=result), request)
    except Exception as e:
        return await jsonResponse(await return_params(message='network error {}'.format(e), code=Code.NETWORK), request)


# 删除日志
async def remove(params, request):
    try:
        count = delete_log(params)
        if count > 0:
            return await jsonResponse(
                await return_params(lists=params, message='remove system log successfully'), request)
        return await jsonResponse(
            await return_params(lists=params, message='remove system log failed', code=Code.ERROR), request)
    except Exception as e:
        return await jsonResponse(await return_params(message='network error {}'.format(e), code=Code.NETWORK), request)
