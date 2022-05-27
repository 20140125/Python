#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services import common

router = APIRouter()


# 生成验证码（随机数）
@router.post('/common/captcha')
async def captcha(request: Request):
    return await common.captcha(request)
