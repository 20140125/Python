#!/usr/bin/python3
import random
from typing import Union

from pydantic import BaseModel, EmailStr


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
    token: Union[str, None]


# 分页查询信息
class paginationModel(BaseModel):
    page: Union[int] = 1
    limit: Union[int] = 10
    token: Union[str, None]


# 根据ID删除记录
class deleteModel(BaseModel):
    id: Union[int] = 1
    token: Union[str, None]


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


# 简单搜索模型
class searchModel(BaseModel):
    id: Union[int] = 1
    token: Union[str, None]
