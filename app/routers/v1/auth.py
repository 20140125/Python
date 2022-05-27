#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.v1 import auth
from db import schemas

router = APIRouter()


# 获取权限列表
@router.post('/auth/lists')
async def lists(params: schemas.paginationModel, request: Request):
    return await auth.lists(params, request)


@router.post('/auth/save')
async def save(params: schemas.authModel, request: Request):
    return await auth.save(params, request)
