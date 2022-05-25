#!/usr/bin/python3

from app.middleware.config import MiddlewareMessage
from db.crud.Auth import get_auth_lists
from tools.helper import jsonResponse, return_params

Code = MiddlewareMessage()


# 获取权限列表
async def lists(params, request):
    try:
        item = get_auth_lists(params.page, params.limit)
        return await jsonResponse(await return_params(lists=item), request)
    except Exception as e:
        return await jsonResponse(await return_params(message='network error {}'.format(e), code=Code.NETWORK), request)
