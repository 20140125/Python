#!/usr/bin/python3
from pydantic import BaseModel


class LogModel(BaseModel):
    username: str
    url: str
    ip_address: str
    log: str
    created_at: int
    day: str
    local: str


class Pagination(BaseModel):
    page: int = 1
    limit: int = 1000
