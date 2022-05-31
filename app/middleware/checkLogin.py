#!/usr/bin/python3
import json
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

import db.models as models
from db.crud import users, role as roles
from tools import helper
from tools.redis import redisClient

"""
todo：设置主体内容
app.middleware.checkLogin async
def set_body(request: {receive, _receive}) -> Coroutine[Any, Any, None]
"""


async def set_body(request):
    receive_ = await request.receive()

    async def receive():
        return receive_

    request._receive = receive


"""
todo：校验登录权限
app.middleware.checkLogin class 
checkLogin(BaseHTTPMiddleware)
"""


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
        # post请求，数据格式 application/json
        if request.headers.get('Content-Type') == 'application/json':
            # 需要登录的地址
            if not (request.url.path in helper.code.NOT_LOGIN_ACCESS_URL):
                params = await request.json()
                # 判断用户否登录系统
                if not ('token' in params):
                    return await helper.jsonResponse(request, status=helper.code.UNAUTHORIZED,
                                                     message=helper.code.NOT_LOGIN_MESSAGE)
                #  请求头必须带上Authentication验证用户合法性
                if not ('authentication' in request.headers):
                    return await helper.jsonResponse(request, status=helper.code.UNAUTHORIZED,
                                                     message=helper.code.TOKEN_EMPTY_MESSAGE)
                # 判断Redis是否有这个用户
                if await redisClient.get_value(params['token']) is None:
                    return await helper.jsonResponse(request, status=helper.code.UNAUTHORIZED,
                                                     message=helper.code.TOKEN_EMPTY_MESSAGE)
                user = users.get([models.Users.remember_token == params['token']])
                # 用户账号非法
                if user is None:
                    return await helper.jsonResponse(request, status=helper.code.FORBIDDEN,
                                                     message=helper.code.FORBIDDEN_MESSAGE)
                # 用户被禁用
                if user['status'] == 2:
                    return await helper.jsonResponse(request, status=helper.code.UNAUTHORIZED,
                                                     message=helper.code.USER_DISABLED_MESSAGE)
                role = roles.get([models.Role.id == user['role_id']])
                # 角色不存在
                if role is None:
                    return await helper.jsonResponse(request, status=helper.code.UNAUTHORIZED,
                                                     message=helper.code.ROLE_NOT_EXIST_MESSAGE)
                # 角色被禁用
                if role['status'] == 2:
                    return await helper.jsonResponse(request, status=helper.code.UNAUTHORIZED,
                                                     message=helper.code.ROLE_DISABLED_MESSAGE)
                # 如果用户不是超级管理员
                if role['id'] != 1:
                    if not (request.url.path in json.loads(role['auth_api'])):
                        return await helper.jsonResponse(request, status=helper.code.UNAUTHORIZED,
                                                         message=helper.code.FORBIDDEN_MESSAGE)

        # process the request and get the response
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        if request.headers.get('Content-Type') == 'application/json':
            if not (request.url.path in helper.code.NOT_LOGIN_ACCESS_URL):
                response.headers['Authentication'] = params['token']
        return response
