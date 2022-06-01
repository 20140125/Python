#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

# 声明基类
Base = declarative_base()


def to_json(this):
    return {c.name: getattr(this, c.name, None) for c in this.__table__.columns}


# 权限
class Auth(Base):
    __tablename__ = 'os_auth'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    href = Column(String(length=255))
    api = Column(String(length=255))
    pid = Column(Integer, index=True)
    path = Column(String(length=255))
    level = Column(Integer)
    status = Column(Integer)


# 角色
class Role(Base):
    __tablename__ = 'os_role'
    id = Column(Integer, primary_key=True)
    role_name = Column(String(length=64), index=True)
    auth_ids = Column(Text)
    auth_api = Column(Text)
    status = Column(Integer)
    created_at = Column(Integer)
    updated_at = Column(Integer)


# 日志
class Log(Base):
    __tablename__ = 'os_system_log'
    id = Column(Integer, primary_key=True)
    username = Column(String(length=32), index=True)
    url = Column(String(length=64))
    ip_address = Column(String(length=32), index=True)
    log = Column(Text)
    created_at = Column(Integer)
    day = Column(String(length=16))
    local = Column(String(length=128))


# 用户
class Users(Base):
    __tablename__ = 'os_users'
    id = Column(Integer, primary_key=True)
    username = Column(String(length=64))
    email = Column(String(length=32))
    role_id = Column(Integer())
    ip_address = Column(String(length=32))
    status = Column(Integer())
    created_at = Column(Integer())
    updated_at = Column(Integer())
    password = Column(String(length=32))
    salt = Column(String(length=8))
    remember_token = Column(String(length=1000))
    phone_number = Column(String(length=11))
    avatar_url = Column(String(length=512))
    uuid = Column(String(length=128))
    char = Column(String(length=1))


# 个人中心
class UsersCenter(Base):
    __tablename__ = 'os_users_center'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, index=True)
    u_name = Column(String(length=64))
    tags = Column(String(length=128))
    local = Column(String(length=64))
    ip_address = Column(String(length=32))
    notice_status = Column(Integer)
    user_status = Column(Integer)
    desc = Column(String(length=128))
    token = Column(String(length=1000))
