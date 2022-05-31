#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.v1 import users
from db import schemas

router = APIRouter()

"""
todo: 角色列表
Parameter params, request of app.routers.v1.users.lists
params: paginationModel
request: Request
return JSONResponse
"""


@router.post('/account/lists')
async def lists(params: schemas.paginationModel, request: Request):
    return await users.lists(params, request)


"""
todo: 登录系统
Parameter params, request of app.routers.v1.users.login
params: loginModel
request: Request
return JSONResponse
"""


@router.post('/account/login')
async def login(params: schemas.loginModel, request: Request):
    return await users.login(params, request)


"""
todo: 登出系统
Parameter params, request of app.routers.v1.users.logout
params: logoutModel
request: Request
return JSONResponse
"""


@router.post('/account/logout')
async def logout(params: schemas.logoutModel, request: Request):
    return await users.logout(params, request)


"""
todo: 注册用户
Parameter params, request of app.routers.v1.users.register
params: registerModel
request: Request
return JSONResponse
"""


@router.post('/account/register')
async def register(params: schemas.registerModel, request: Request):
    return await users.register(params, request)
