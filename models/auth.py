#!/usr/bin/python3
from typing import Union

from pydantic import BaseModel


# 更新权限
class authModel(BaseModel):
    id: Union[int] = 0
    name: Union[str, None]
    href: Union[str, None]
    api: Union[str, None]
    pid: Union[int] = 0
    path: Union[str, None]
    level: Union[int] = 0
    status: Union[int] = 1
