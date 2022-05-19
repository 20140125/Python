#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.users import (login, logout, register, set_verify_code)
from models.users import (login, logout, register)

router = APIRouter()


# 生成验证码（随机数）
@router.post('/api/v1/common/verify-code', tags=['Common Authentication'])
async def get_verify_code(request: Request):
    return await set_verify_code()


# 登录系统
@router.post('/api/v1/account/login', tags=['Account'])
async def login_system(user: login):
    return await login(user)


# 登出系统
@router.post('/api/v1/account/logout', tags=['Account'])
async def logout_system(user: logout):
    return await logout(user)


# 注册用户
@router.post('/api/v1/account/register', tags=['Account'])
async def register_system(user: register):
    return await register(user)
