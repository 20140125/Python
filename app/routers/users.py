#!/usr/bin/python3

from fastapi import APIRouter, Request, Depends

from app.services.users import (login, logout, register, captcha)
import db.schemas as schemas
from db.alchemyConnection import Session


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


# 生成验证码（随机数）
@router.post('/api/v1/common/captcha', tags=['Common Authentication'])
async def get_captcha(request: Request):
    return await captcha(request)


# 登录系统
@router.post('/api/v1/account/login', tags=['Account'])
async def login_system(users: schemas.loginModel, request: Request):
    return await login(users, request)


# 登出系统
@router.post('/api/v1/account/logout', tags=['Account'])
async def logout_system(users: schemas.logoutModel, request: Request):
    return await logout(users, request)


# 注册用户
@router.post('/api/v1/account/register', tags=['Account'])
async def register_system(users: schemas.registerModel, request: Request):
    return await register(users, request)
