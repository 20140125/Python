#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.v1 import auth
from db import schemas

router = APIRouter()

"""
todo: 获取权限列表
Parameter params, request of app.routers.v1.auth.lists
params: paginationModel
request: Request
return JSONResponse
"""


@router.post('/auth/lists')
async def lists(params: schemas.paginationModel, request: Request):
    return await auth.lists(params, request)


"""
todo: 保存权限
Parameter params, request of app.routers.v1.auth.save
params: authModel
request: Request
return JSONResponse
"""


@router.post('/auth/save')
async def save(params: schemas.authModel, request: Request):
    return await auth.save(params, request)
