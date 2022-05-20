#!/usr/bin/python3

from app.middleware.config import MiddlewareMessage
from db.connection import MySQLdb

Code = MiddlewareMessage()


# 获取权限列表
async def lists(pagination):
    try:
        item = MySQLdb.get_lists(
            'select id, name, href, api, pid, path, level, status from os_auth order by path limit %s, %s',
            (pagination.limit * (pagination.page - 1), pagination.limit))
        return {'message': 'successfully', 'code': Code.SUCCESS, 'lists': item}
    except Exception as e:
        return {'message': 'network error {}'.format(e), 'code': Code.NETWORK}
