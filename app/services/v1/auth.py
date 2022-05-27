#!/usr/bin/python3

import db.crud.auth as auth_services
import db.models as models
import tools.helper as helper
from app.middleware.config import MiddlewareMessage

Code = MiddlewareMessage()


# 获取权限列表
async def lists(params, request):
    try:
        item = auth_services.get_auth_lists(params.page, params.limit)
        return await helper.jsonResponse(await helper.return_params(lists=item), request)
    except Exception as e:
        return await helper.jsonResponse(
            await helper.return_params(message='network error {}'.format(e), code=Code.NETWORK), request)


# 保存权限
async def save(params, request):
    try:
        params.id = auth_services.save_auth(params)
        if params.id is None:
            return await helper.jsonResponse(await helper.return_params(code=Code.ERROR), request)
        item = auth_services.get_one_auth([models.Auth.id == params.id])
        params.path = params.id
        params.level = 0
        if item is not None:
            params.path = item['path'] + '-' + params.id
            params.level = params.path.count('-')
        res = auth_services.update_auth(params)
        if res is None:
            return await helper.jsonResponse(await helper.return_params(code=Code.ERROR), request)
        return await helper.jsonResponse(await helper.return_params(lists=params), request)
    except Exception as e:
        return await helper.jsonResponse(
            await helper.return_params(message='network error {}'.format(e), code=Code.NETWORK), request)
