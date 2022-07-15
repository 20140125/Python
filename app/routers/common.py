#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services import common
from db import schemas

router = APIRouter()


@router.post('/common/captcha')
async def captcha(request: Request):
    """
    todo: 验证码
    :param request:
    :return JSONResponse:
    """
    return await common.captcha(request)


@router.post('/common/token')
async def set_token(params: schemas.logoutModel, request: Request):
    """
    todo: 保存TOKEN
    :param params:
    :param request:
    :return JSONResponse:
    """
    return await common.set_token(params, request)
