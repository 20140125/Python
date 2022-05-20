#!/usr/bin/python3
import json


from app.middleware.config import MiddlewareMessage
from db.connection import MySQLdb
from tools.helper import jsonResponse

Code = MiddlewareMessage()


# 获取日志列表
async def lists(pagination, request):
    try:
        item = MySQLdb.get_lists(
            'select id, username, url, ip_address, log, created_at, day, local from os_system_log order by id desc limit %s, %s',
            (pagination.limit * (pagination.page - 1), pagination.limit))
        if item is not None:
            for data in item:
                data['log'] = json.loads(data['log'])
        info = {'message': 'successfully', 'code': Code.SUCCESS, 'lists': item}
    except Exception as e:
        info = {'message': 'network error {}'.format(e), 'code': Code.NETWORK, 'lists': []}
    return await jsonResponse(info, request)


# 删除日志
async def remove(params, request):
    try:
        count = MySQLdb.update_one('delete from os_system_log where id = %s', (params.id,))
        if count > 0:
            info = {'message': 'successfully', 'code': Code.SUCCESS, 'lists': params}
        else:
            info = {'message': 'remove system log failed', 'code': Code.ERROR, 'lists': params}
        return await jsonResponse(info, request)
    except Exception as e:
        info = {'message': 'network error {}'.format(e), 'code': Code.NETWORK, 'lists': []}
    return info

