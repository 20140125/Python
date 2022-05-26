#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.systemLog import (lists, remove)
import db.schemas as schemas

router = APIRouter()


# 获取日志列表
@router.post('/api/v1/log/lists', tags=['systemLog'])
async def log_lists(params: schemas.paginationModel, request: Request):
    return await lists(params, request)


# 删除日志
@router.post('/api/v1/log/remove', tags=['systemLog'])
async def remove_log(params: schemas.deleteModel, request: Request):
    return await remove(params, request)
