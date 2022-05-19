#!/usr/bin/python3

from fastapi import APIRouter

from app.services.users import (login, logout, register, set_verify_code)

from models.users import (UserLogin, userLogout, registerUser)

router = APIRouter()


# 生成验证码（随机数）
@router.post('/api/v1/common/verify-code', tags=['common'])
async def get_verify_code():
    return await set_verify_code()


# 登录系统
@router.post('/api/v1/account/login', tags=['users'])
async def login_system(user: UserLogin):
    return await login(user)


# 登出系统
@router.post('/api/v1/account/logout', tags=['users'])
async def logout_system(user: userLogout):
    return await logout(user)


# 注册用户
@router.post('/api/v1/account/register', tags=['users'])
async def register_system(user: registerUser):
    return await register(user)
