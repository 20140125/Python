#!/usr/bin/python3

from db.crud import auth
from db import models
from tools import helper


# 获取权限列表
async def lists(params, request):
    try:
        item = auth.lists(params.page, params.limit)
        return await helper.jsonResponse(request, lists=item)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


# 保存权限
async def save(params, request):
    try:
        params.id = auth.save(params)
        if params.id is None:
            return await helper.jsonResponse(status=helper.code.ERROR, message='save auth error')
        item = auth.get([models.Auth.id == params.pid])
        params.path = str(params.id)
        params.level = 0
        if item is not None:
            params.path = '{}-{}'.format(item['path'], str(params.id))
            params.level = params.path.count('-')
        if auth.update(params):
            return await helper.jsonResponse(request, lists=({'id': params.id}))
        return await helper.jsonResponse(request, status=helper.code.ERROR, message='update auth error')
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)
