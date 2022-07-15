#!/usr/bin/python3
from tools import helper


async def lists(request, filepath):
    """
    todo:获取文件列表
    :param request:
    :param filepath:
    :return JSONResponse:
    """
    try:
        return await helper.jsonResponse(request, lists=await helper.get_file_list(filepath))
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


async def get(request, filepath):
    """
       todo:获取文件内容
       :param request:
       :param filepath:
       :return JSONResponse:
       """
    try:
        return await helper.jsonResponse(request, lists={'content': await helper.get_file_content(filepath)})
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)


async def write(request, filepath, content):
    """
       todo:写入文件内容
       :param request:
       :param content:
       :param filepath:
       :return JSONResponse:
       """
    try:
        await helper.write_file_content(filepath, content)
        return await helper.jsonResponse(request)
    except Exception as e:
        return await helper.jsonResponse(request, message='network error {}'.format(e), status=helper.code.NETWORK)
