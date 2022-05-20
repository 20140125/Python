#!/usr/bin/python3

from fastapi import APIRouter

from app.services.auth import (lists)
from models.systemLog import Pagination

router = APIRouter()


# 获取权限列表
@router.post('/api/v1/auth/lists', tags=['Authentication'])
async def auth_lists(pagination: Pagination):
    return await lists(pagination)
