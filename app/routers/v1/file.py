from fastapi import APIRouter, Request

from app.services.v1 import file
from db import schemas

router = APIRouter()


@router.post('/file/lists')
async def lists(params: schemas.fileListsModel, request: Request):
    """
    todo: 获取文件列表
    :param params:
    :param request:
    :return JSONResponse:
    """
    return await file.lists(request, params.filepath)


@router.post('/file/get')
async def get(params: schemas.fileListsModel, request: Request):
    """
    todo: 获取文件内容
    :param params:
    :param request:
    :return JSONResponse:
    """
    return await file.get(request, params.filepath)


@router.post('/file/write')
async def write(params: schemas.fileWriterModel, request: Request):
    """
    todo: 获取文件内容
    :param params:
    :param request:
    :return JSONResponse:
    """
    print(params)
    return await file.write(request, params.filepath, params.content)
