from datetime import datetime, timedelta

import jwt
from fastapi import FastAPI

from config.app import Settings

# 获取配置信息
config = Settings()

# app
app = FastAPI()


# 生成token
async def create_access_token(data: dict):
    to_encode = data.copy()
    # token失效时限
    expire = datetime.utcnow() + timedelta(minutes=config.access_token_expire_minutes)
    # 更新到我们之前传进来的字典
    to_encode.update({'exp': expire})
    # jwt 编码 生成我们需要的token
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.token_algorithm)
    # 返回token信息
    return encoded_jwt
