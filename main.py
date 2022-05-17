from typing import Union

from fastapi import FastAPI

from MysqlConnection import MySQLdb

from pydantic import BaseModel, EmailStr

import json

# 项目初始化
app = FastAPI(debug=True)
# 数据库初始化
MySQLdb = MySQLdb('localhost', 'root', '123456789', 'longer')


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.post('/login')
def login():
    try:
        username = 'admin'
        res = MySQLdb.get_one("SELECT * FROM os_users WHERE username = %s", (username,))
        info = {'message': 'successfully', 'code': 200, 'item': res}
    except Exception as e:
        info = {'message': e, 'code': 500, 'item': []}
    return info


@app.get('/logs/{version}')
def get_logs(page: Union[int, None] = 1, limit: Union[int, None] = 10):
    try:
        res = MySQLdb.get_lists("select * from os_system_log order by id desc limit %s, %s",
                                 (limit * (page - 1), limit))
        for item in res:
            item['log'] = json.loads(item['log'])
        info = {'message': 'successfully', 'code': 200, 'item': res}
    except Exception as e:
        info = {'message': e, 'code': 500}
    return info


class userIn(BaseModel):
    username: str


class userOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role_id: int
    ip_address: str
    status: int
    created_at: int
    updated_at: int
    password: str
    salt: str
    remember_token: str
    phone_number: str
    avatar_url: str
    uuid: str
    char: str


@app.post('/post', response_model=userOut)
async def get_user(user: userIn):
    return MySQLdb.get_one("SELECT * FROM os_users WHERE username = %s", (user.username,))


