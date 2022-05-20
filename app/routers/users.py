#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.users import (login, logout, register, captcha)
from models.users import (loginModel, logoutModel, registerModel)

router = APIRouter()


# 生成验证码（随机数）
@router.post('/api/v1/common/captcha', tags=['Common Authentication'])
async def get_captcha(request: Request):
    return await captcha(request)


# 登录系统
@router.post('/api/v1/account/login', tags=['Account'])
async def login_system(users: loginModel, request: Request):
    return await login(users, request)


# 登出系统
@router.post('/api/v1/account/logout', tags=['Account'])
async def logout_system(users: logoutModel, request: Request):
    return await logout(users, request)


# 注册用户
@router.post('/api/v1/account/register', tags=['Account'])
async def register_system(users: registerModel, request: Request):
    return await register(users, request)
