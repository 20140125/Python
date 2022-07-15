#!/usr/bin/python3
from db.crud import image
from tools import helper


async def lists(params, request):
    """
    todo:获取图片列表
    :param params:
    :param request:
    :return:
    """
    try:
        item = image.lists(params.page, params.limit)
        return await helper.jsonResponse(request, lists=item)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)
