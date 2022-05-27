#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.v1 import systemLog
from db import schemas

router = APIRouter()


# 获取日志列表
@router.post('/log/lists')
async def lists(params: schemas.paginationModel, request: Request):
    return await systemLog.lists(params, request)


# 删除日志
@router.post('/log/remove')
async def remove(params: schemas.deleteModel, request: Request):
    return await systemLog.remove(params, request)
