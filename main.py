#!/usr/bin/python3

from fastapi import FastAPI

import app.routers as router
from app.middleware.checkLogin import checkLogin

app = FastAPI()
# 自定义中间件
app.add_middleware(checkLogin)
# 路由注册
app.include_router(router.router, prefix='/api/v1')
