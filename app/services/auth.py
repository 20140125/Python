#!/usr/bin/python3

from app.middleware.config import MiddlewareMessage
from db.connection import MySQLdb
from tools.helper import jsonResponse, return_params

Code = MiddlewareMessage()


# 获取权限列表
async def lists(params, request):
    try:
        item = MySQLdb.get_lists(
            'select id, name, href, api, pid, path, level, status from os_auth order by path limit %s, %s',
            (params.limit * (params.page - 1), params.limit))
        return await jsonResponse(await return_params(lists=item), request)
    except Exception as e:
        return await jsonResponse(await return_params(message='network error {}'.format(e), code=Code.NETWORK), request)


