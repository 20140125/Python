#!/usr/bin/python3

from fastapi import APIRouter, Request

import app.services.v1.auth as auth_services
import db.schemas as schemas

router = APIRouter()


# 获取权限列表
@router.post('/auth/lists')
async def auth_lists(params: schemas.paginationModel, request: Request):
    return await auth_services.lists(params, request)


@router.post('/auth/save')
async def save_auth(params: schemas.authModel, request: Request):
    return await auth_services.save(params, request)
