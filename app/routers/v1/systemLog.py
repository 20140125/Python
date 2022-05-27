#!/usr/bin/python3

from fastapi import APIRouter, Request

import app.services.v1.systemLog as log_services
import db.schemas as schemas

router = APIRouter()


# 获取日志列表
@router.post('/log/lists')
async def log_lists(params: schemas.paginationModel, request: Request):
    return await log_services.lists(params, request)


# 删除日志
@router.post('/log/remove')
async def remove_log(params: schemas.deleteModel, request: Request):
    return await log_services.remove(params, request)
