#!/usr/bin/python3

from fastapi import APIRouter, Request

from app.services.v1 import image
from db import schemas

router = APIRouter()


@router.post('/image/lists')
async def lists(params: schemas.paginationModel, request: Request):
    """
    todo: 获取图片列表
    :param params:
    :param request:
    :return JSONResponse:
    """
    return await image.lists(params, request)
