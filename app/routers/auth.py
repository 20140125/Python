#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.auth import (lists)
from models.common import Pagination
from models.auth import saveModel

router = APIRouter()


# 获取权限列表
@router.post('/api/v1/auth/lists', tags=['Authentication'])
async def auth_lists(params: Pagination, request: Request):
    return await lists(params, request)


@router.post('/api/v1/auth/save', tags=['Authentication'])
async def save_auth(params: saveModel, request: Request):
    return await lists(params, request)
