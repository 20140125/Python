#!/usr/bin/python3

from db import models
from db.crud import auth
from tools import helper


async def lists(params, request):
    """
    todo：获取权限列表
    :param params:
    :param request:
    :return JSONResponse:
    """
    try:
        item = auth.lists(params.page, params.limit)
        return await helper.jsonResponse(request, lists=item)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


async def save(params, request):
    """
    todo：保存权限
    :param params:
    :param request:
    :return JSONResponse:
    """
    try:
        auth_model = models.Auth(
            name=params.name,
            href=params.href,
            status=params.status,
            pid=params.pid,
            api=params.href.replace('/admin/', '/api/v1/')
        )
        auth_id = auth.save(auth_model)
        if auth_id is None:
            return await helper.jsonResponse(request, status=helper.code.ERROR)
        result = auth.get([models.Auth.id == params.pid])
        path = str(auth_id)
        level = 0
        if result is not None:
            path = '{}-{}'.format(result['path'], str(auth_id))
            level = params.path.count('-')
        if auth.update(models.Auth(path=path, level=level, id=auth_id)):
            return await helper.jsonResponse(request, lists=(models.to_json(auth_model)))
        return await helper.jsonResponse(request, status=helper.code.ERROR)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)
