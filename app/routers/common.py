#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services import common

router = APIRouter()

"""
todo: 验证码
Parameter request of app.routers.common.captcha
request: Request
return JSONResponse
"""


@router.post('/common/captcha')
async def captcha(request: Request):
    return await common.captcha(request)
