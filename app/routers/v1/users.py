#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.v1 import users
from db import schemas

router = APIRouter()


@router.post('/account/lists')
async def lists(params: schemas.paginationModel, request: Request):
    """
    todo: 角色列表
    :param params:
    :param request:
    :return JSONResponse:
    """
    return await users.lists(params, request)


@router.post('/account/login')
async def login(params: schemas.loginModel, request: Request):
    """
    todo: 登录系统
    :param params:
    :param request:
    :return JSONResponse:
    """
    return await users.login(params, request)


@router.post('/account/logout')
async def logout(params: schemas.logoutModel, request: Request):
    """
    todo: 登出系统
    :param params:
    :param request:
    :return JSONResponse:
    """
    return await users.logout(params, request)


@router.post('/account/register')
async def register(params: schemas.registerModel, request: Request):
    """
    todo: 注册用户
    :param params:
    :param request:
    :return JSONResponse:
    """
    return await users.register(params, request)
