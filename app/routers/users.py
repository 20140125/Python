#!/usr/bin/python3

from fastapi import APIRouter

from app.services.users import (login, logout, register, verify_code)
from models.users import (loginModel, logoutModel, registerModel)

router = APIRouter()


# 生成验证码（随机数）
@router.get('/api/v1/common/verify_code', tags=['Common Authentication'])
async def get_verify_code():
    return await verify_code()


# 登录系统
@router.post('/api/v1/account/login', tags=['Account'])
async def login_system(users: loginModel):
    return await login(users)


# 登出系统
@router.post('/api/v1/account/logout', tags=['Account'])
async def logout_system(users: logoutModel):
    return await logout(users)


# 注册用户
@router.post('/api/v1/account/register', tags=['Account'])
async def register_system(users: registerModel):
    return await register(users)
