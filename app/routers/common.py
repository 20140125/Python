#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services import common

router = APIRouter()


@router.post('/common/captcha')
async def captcha(request: Request):
    """
    todo: 验证码
    :param request:
    :return JSONResponse:
    """
    return await common.captcha(request)
