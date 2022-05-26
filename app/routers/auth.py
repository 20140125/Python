#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.auth import (lists)
import db.schemas as schemas


router = APIRouter()


# 获取权限列表
@router.post('/api/v1/auth/lists', tags=['Authentication'])
async def auth_lists(params: schemas.paginationModel, request: Request):
    return await lists(params, request)


@router.post('/api/v1/auth/save', tags=['Authentication'])
async def save_auth(params: schemas.authModel, request: Request):
    return await lists(params, request)
