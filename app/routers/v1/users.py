#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.v1 import users
from db import schemas

router = APIRouter()


# 注册用户
@router.post('/account/lists')
async def lists(params: schemas.paginationModel, request: Request):
    return await users.lists(params, request)


# 登录系统
@router.post('/account/login')
async def login(params: schemas.loginModel, request: Request):
    return await users.login(params, request)


# 登出系统
@router.post('/account/logout')
async def logout(params: schemas.logoutModel, request: Request):
    return await users.logout(params, request)


# 注册用户
@router.post('/account/register')
async def register(params: schemas.registerModel, request: Request):
    return await users.register(params, request)
