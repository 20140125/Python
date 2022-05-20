#!/usr/bin/python3
import random
from typing import Union

from pydantic import BaseModel, EmailStr


# 登录系统
class loginModel(BaseModel):
    email: EmailStr
    password: Union[str, None]
    captcha: Union[int] = random.randint(100000, 999999)


# 登出系统
class logoutModel(BaseModel):
    token: Union[str, None]


# 邮箱账号注册用户
class registerModel(BaseModel):
    email: EmailStr
    captcha: Union[int] = random.randint(100000, 999999)
