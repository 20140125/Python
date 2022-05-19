#!/usr/bin/python3
import random

from pydantic import BaseModel, EmailStr


# 登录系统
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    verify_code: str = random.randint(100000, 999999)


# 登出系统
class userLogout(BaseModel):
    remember_token: str


# 邮箱账号注册用户
class registerUser(BaseModel):
    email: EmailStr
    verify_code: int

