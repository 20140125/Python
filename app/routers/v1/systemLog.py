#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.v1 import systemLog
from db import schemas

router = APIRouter()

"""
todo: 获取日志列表
Parameter params, request of app.routers.v1.systemLog.lists
params: paginationModel
request: Request
return JSONResponse
"""


@router.post('/log/lists')
async def lists(params: schemas.paginationModel, request: Request):
    return await systemLog.lists(params, request)


"""
todo: 删除日志
Parameter params, request of app.routers.v1.systemLog.remove
params: deleteModel
request: Request
return JSONResponse
"""


@router.post('/log/remove')
async def remove(params: schemas.deleteModel, request: Request):
    return await systemLog.remove(params, request)
