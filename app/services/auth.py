#!/usr/bin/python3

from app.middleware.config import MiddlewareMessage
from db.crud.auth import get_auth_lists, save_auth, get_one_auth, update_auth
from db.orm.auth import auth
from tools.helper import jsonResponse, return_params

Code = MiddlewareMessage()


# 获取权限列表
async def lists(params, request):
    try:
        item = get_auth_lists(params.page, params.limit)
        return await jsonResponse(await return_params(lists=item), request)
    except Exception as e:
        return await jsonResponse(await return_params(message='network error {}'.format(e), code=Code.NETWORK), request)


# 保存权限
async def save(params, request):
    try:
        params.id = save_auth(params)
        if params.id is None:
            return await jsonResponse(await return_params(code=Code.ERROR), request)
        item = get_one_auth([auth.id == params.id])
        params.path = params.id
        params.level = 0
        if item is not None:
            params.path = item['path'] + '-' + params.id
            params.level = params.path.count('-')
        res = update_auth(params)
        if res is None:
            return await jsonResponse(await return_params(code=Code.ERROR), request)
        return await jsonResponse(await return_params(lists=params), request)
    except Exception as e:
        return await jsonResponse(await return_params(message='network error {}'.format(e), code=Code.NETWORK), request)
