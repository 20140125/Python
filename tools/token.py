from datetime import datetime, timedelta

from fastapi import FastAPI
import jwt

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# app
app = FastAPI()


# 生成token
def create_access_token(data: dict):
    to_encode = data.copy()
    # token失效时限
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 更新到我们之前传进来的字典
    to_encode.update({'exp': expire})
    # jwt 编码 生成我们需要的token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # 返回token信息
    return encoded_jwt


