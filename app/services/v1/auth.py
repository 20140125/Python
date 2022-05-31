#!/usr/bin/python3

from db import models
from db.crud import auth
from tools import helper

"""
todo：获取权限列表
Parameter params of app.services.v1.auth.lists 
params: {page, limit}
request: {url, headers, client}
return JSONResponse
"""


async def lists(params, request):
    try:
        item = auth.lists(params.page, params.limit)
        return await helper.jsonResponse(request, lists=item)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


"""
todo：保存权限
Parameter params， request of app.services.v1.auth.save
params: {id, api, href, name, status, pid, path, level}
request: {url, headers, client}
return JSONResponse
"""


async def save(params, request):
    try:
        params.id = auth.save(models.Auth(
            name=params.name,
            href=params.href,
            status=params.status,
            pid=params.pid,
            api=params.href.replace('/admin/', '/api/v1/')
        ))
        if params.id is None:
            return await helper.jsonResponse(request, status=helper.code.ERROR)
        result = auth.get([models.Auth.id == params.pid])
        params.path = str(params.id)
        params.level = 0
        if result is not None:
            params.path = '{}-{}'.format(result['path'], str(params.id))
            params.level = params.path.count('-')
        if auth.update(params):
            return await helper.jsonResponse(request, lists=({'id': params.id}))
        return await helper.jsonResponse(request, status=helper.code.ERROR)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)
