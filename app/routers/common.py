#!/usr/bin/python3

from fastapi import APIRouter, Request

import app.services.common as common

router = APIRouter()


# 生成验证码（随机数）
@router.post('/common/captcha')
async def get_captcha(request: Request):
    return await common.captcha(request)
