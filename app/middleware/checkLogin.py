#!/usr/bin/python3
import json
import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.middleware.config import MiddlewareMessage
from db.connection import MySQLdb
from tools.redis import redisClient

ERR_MSG = MiddlewareMessage()


# 设置主体内容
async def set_body(request):
    receive_ = await request.receive()

    async def receive():
        return receive_

    request._receive = receive


# 校验登录权限
class checkLogin(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    # 重写基础中间件
    async def dispatch(self, request: Request, call_next):
        # 保证程序可以向下进行
        await set_body(request)
        # 请求开始时间
        start_time = time.time()
        # do something with the request object
        # 保证请求的数据是JSON
        params = None

        if request.headers.get('Content-Type') == 'application/json' and not (
                request.url.path in ERR_MSG.NOT_LOGIN_ACCESS_URL):
            params = await request.json()
            # 判断用户否登录系统
            if not ('token' in params):
                return Response(ERR_MSG.NOT_LOGIN_MESSAGE)
            #  请求头必须带上Authentication验证用户合法性
            # if not ('authentication' in request.headers):
            #     return Response(ERR_MSG.TOKEN_EMPTY_MESSAGE)
            # 判断Redis是否有这个用户
            if await redisClient.get_value(params['token']) is None:
                return Response(ERR_MSG.TOKEN_EMPTY_MESSAGE)
            users = MySQLdb.get_one('select * from os_users where remember_token = %s', (params['token']))
            # 用户账号非法
            if users is None:
                return Response(ERR_MSG.FORBIDDEN)
            # 用户被禁用
            if users['status'] == 2:
                return Response(ERR_MSG.USER_DISABLED_MESSAGE)
            role = MySQLdb.get_one('select auth_api, status, id from os_role where id = %s', (users['role_id']))
            # 角色不存在
            if role is None:
                return Response(ERR_MSG.ROLE_NOT_EXIST_MESSAGE)
            # 角色被禁用
            if role['status'] == 2:
                return Response(ERR_MSG.ROLE_DISABLED_MESSAGE)
            # 如果用户不是超级管理员
            if role['id'] != 1:
                if not (request.url.path in json.loads(role['auth_api'])):
                    return Response(ERR_MSG.FORBIDDEN_MESSAGE)

        # process the request and get the response
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        if request.headers.get('Content-Type') == 'application/json' and not (
                request.url.path in ERR_MSG.NOT_LOGIN_ACCESS_URL):
            response.headers['Authentication'] = params['token']
        return response
