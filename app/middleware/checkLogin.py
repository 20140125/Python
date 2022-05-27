#!/usr/bin/python3
import json
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

import db.models as models
from app.middleware.config import MiddlewareMessage
from db.crud.role import get_one_role
from db.crud.users import get_one_user
import tools.helper as helper
from tools.redis import redisClient

Code = MiddlewareMessage()


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
        # post请求，数据格式 application/json
        if request.headers.get('Content-Type') == 'application/json':
            # 需要登录的地址
            if not (request.url.path in Code.NOT_LOGIN_ACCESS_URL):
                params = await request.json()
                # 判断用户否登录系统
                if not ('token' in params):
                    return await helper.jsonResponse(
                        await helper.return_params(code=Code.UNAUTHORIZED, message=Code.NOT_LOGIN_MESSAGE), request)
                #  请求头必须带上Authentication验证用户合法性
                # if not ('authentication' in request.headers):
                #     return await jsonResponse(
                #         await return_params(code=Code.UNAUTHORIZED, message=Code.TOKEN_EMPTY_MESSAGE), request)
                # 判断Redis是否有这个用户
                if await redisClient.get_value(params['token']) is None:
                    return await helper.jsonResponse(
                        await helper.return_params(code=Code.UNAUTHORIZED, message=Code.TOKEN_EMPTY_MESSAGE), request)
                user = get_one_user([models.Users.remember_token == params['token']])
                # 用户账号非法
                if user is None:
                    return await helper.jsonResponse(
                        await helper.return_params(code=Code.FORBIDDEN, message=Code.FORBIDDEN_MESSAGE), request)
                # 用户被禁用
                if user['status'] == 2:
                    return await helper.jsonResponse(
                        await helper.return_params(code=Code.UNAUTHORIZED, message=Code.USER_DISABLED_MESSAGE), request)
                item = get_one_role(filters=[models.Role.id == user['role_id']])
                # 角色不存在
                if item is None:
                    return await helper.jsonResponse(
                        await helper.return_params(code=Code.UNAUTHORIZED, message=Code.ROLE_NOT_EXIST_MESSAGE), request)
                # 角色被禁用
                if item['status'] == 2:
                    return await helper.jsonResponse(
                        await helper.return_params(code=Code.UNAUTHORIZED, message=Code.ROLE_DISABLED_MESSAGE), request)
                # 如果用户不是超级管理员
                if item['id'] != 1:
                    if not (request.url.path in json.loads(item['auth_api'])):
                        return await helper.jsonResponse(
                            await helper.return_params(code=Code.UNAUTHORIZED, message=Code.FORBIDDEN_MESSAGE), request)

        # process the request and get the response
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        if request.headers.get('Content-Type') == 'application/json':
            if not (request.url.path in Code.NOT_LOGIN_ACCESS_URL):
                response.headers['Authentication'] = params['token']
        return response
