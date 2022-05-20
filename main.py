#!/usr/bin/python3

from fastapi import FastAPI

from app.middleware.checkLogin import checkLogin
from app.routers import (users, auth, systemLog)

app = FastAPI()
# 自定义中间件
app.add_middleware(checkLogin)
# 路由注册
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(systemLog.router)
