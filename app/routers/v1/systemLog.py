#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.v1 import systemLog
from db import schemas

router = APIRouter()


@router.post('/log/lists')
async def lists(params: schemas.paginationModel, request: Request):
    """
    todo: 获取日志列表
    :param params:
    :param request:
    :return:
    """
    return await systemLog.lists(params, request)


@router.post('/log/remove')
async def remove(params: schemas.deleteModel, request: Request):
    """
    todo: 删除日志
    :param params:
    :param request:
    :return:
    """
    return await systemLog.remove(params, request)
