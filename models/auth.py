#!/usr/bin/python3

from pydantic import BaseModel


class SaveModel(BaseModel):
    name: str
    href: str
    pid: str
    status: int
