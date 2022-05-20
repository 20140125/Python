#!/usr/bin/python3
from typing import Union

from pydantic import BaseModel


class Pagination(BaseModel):
    page: int = 1
    limit: int = 10
    token: Union[str, None]


class DeleteModel(BaseModel):
    id: int = 1
