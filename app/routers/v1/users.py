#!/usr/bin/python3

from fastapi import APIRouter, Request

import app.services.v1.users as users_services
import db.schemas as schemas

router = APIRouter()


# 注册用户
@router.post('/account/lists')
async def register_system(params: schemas.paginationModel, request: Request):
    return await users_services.lists(params, request)


# 登录系统
@router.post('/account/login')
async def login_system(users: schemas.loginModel, request: Request):
    return await users_services.login(users, request)


# 登出系统
@router.post('/account/logout')
async def logout_system(users: schemas.logoutModel, request: Request):
    return await users_services.logout(users, request)


# 注册用户
@router.post('/account/register')
async def register_system(users: schemas.registerModel, request: Request):
    return await users_services.register(users, request)
