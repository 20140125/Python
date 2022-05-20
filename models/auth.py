#!/usr/bin/python3
from typing import Union

from pydantic import BaseModel


class saveModel(BaseModel):
    name: Union[str, None]
    href: Union[str, None]
    pid: Union[str, None]
    status: Union[int] = 1
