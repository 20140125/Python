#!/usr/bin/python3
from typing import Union

from pydantic import BaseModel


# 分页查询信息
class Pagination(BaseModel):
    page: Union[int] = 1
    limit: Union[int] = 10
    token: Union[str, None]


# 根据ID删除记录
class DeleteModel(BaseModel):
    id: Union[int] = 1
    token: Union[str, None]
