#!/usr/bin/python3
import random

from pydantic import BaseModel, EmailStr


# 登录系统
class login(BaseModel):
    email: EmailStr
    password: str
    verify_code: str = random.randint(100000, 999999)


# 登出系统
class logout(BaseModel):
    remember_token: str


# 邮箱账号注册用户
class register(BaseModel):
    email: EmailStr
    verify_code: int
