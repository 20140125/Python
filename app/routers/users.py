#!/usr/bin/python3
from typing import Union

from fastapi import APIRouter

from models.users import (login, logout)

router = APIRouter()


@router.post('/login', tags=['users'])
async def login_system(username: Union[str] = '', password: Union[str] = ''):
    return await login(username, password)


@router.post('/logout', tags=['users'])
async def logout_system(remember_token: Union[str] = ''):
    return await logout(remember_token)
