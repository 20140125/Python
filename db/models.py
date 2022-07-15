#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from config.app import settings

Base = declarative_base()


def to_json(this):
    """
    todo: json转换
    :param this:
    :return:
    """
    return {c.name: getattr(this, c.name, None) for c in this.__table__.columns}


# 权限
class Auth(Base):
    __tablename__ = 'os_auth'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255), default='0')
    href = Column(String(length=255), default='0')
    api = Column(String(length=255), default='0')
    pid = Column(Integer, index=True, default=0)
    path = Column(String(length=255), default='0')
    level = Column(Integer, default=1)
    status = Column(Integer, default=1)


# 角色
class Role(Base):
    __tablename__ = 'os_role'
    id = Column(Integer, primary_key=True)
    role_name = Column(String(length=64), index=True, default='0')
    auth_ids = Column(Text, default='0')
    auth_api = Column(Text, default='0')
    status = Column(Integer, default=1)
    created_at = Column(Integer, default=0)
    updated_at = Column(Integer, default=0)


# 用户
class Users(Base):
    __tablename__ = 'os_users'
    id = Column(Integer, primary_key=True)
    username = Column(String(length=64), default='0')
    email = Column(String(length=32), default='0')
    role_id = Column(Integer, default=2)
    ip_address = Column(String(length=32), default='0')
    status = Column(Integer, default=1)
    created_at = Column(Integer, default=0)
    updated_at = Column(Integer, default=0)
    password = Column(String(length=32), default='0')
    salt = Column(String(length=8), default='0')
    remember_token = Column(String(length=1000), default='0')
    phone_number = Column(String(length=11), default='0')
    avatar_url = Column(String(length=512), default='0')
    uuid = Column(String(length=128), default=settings.default_uuid)
    char = Column(String(length=1), default='0')


# 个人中心
class UsersCenter(Base):
    __tablename__ = 'os_user_center'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, index=True, default=0)
    u_name = Column(String(length=64), default='0')
    tags = Column(String(length=128), default='0')
    local = Column(String(length=64), default='0')
    ip_address = Column(String(length=32), default='0')
    notice_status = Column(Integer, default=1)
    user_status = Column(Integer, default=1)
    desc = Column(String(length=128), default='这个家伙很懒，什么也没有留下！')
    token = Column(String(length=1000))


# 日志
class Log(Base):
    __tablename__ = 'os_system_log'
    id = Column(Integer, primary_key=True)
    username = Column(String(length=32), index=True, default='0')
    url = Column(String(length=64), default='0')
    ip_address = Column(String(length=32), index=True, default='0')
    log = Column(Text, default='0')
    created_at = Column(Integer, default=0)
    day = Column(String(length=16), default='0')
    local = Column(String(length=128), default='0')


# 图片模型
class Image(Base):
    __tablename__ = 'os_soogif'
    id = Column(Integer, primary_key=True)
    href = Column(String(length=256), index=True, default='0')
    name = Column(String(length=256), index=True, default='0')
    width = Column(String(length=8), default='0', index=True)
    height = Column(String(length=8), default='0')


# 图片分类
class ImageType(Base):
    __tablename__ = 'os_soogif_type'
    id = Column(Integer, primary_key=True)
    href = Column(String(length=256), index=True, default='0')
    name = Column(String(length=256), default='0')


# 系统配置
class Config(Base):
    __tablename__ = 'os_system_config'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=32), index=True, default='0')
    children = Column(Text, default='0')
    created_at = Column(Integer, default=0)
    updated_at = Column(Integer, default=0)
    status = Column(Integer, default=1)


# 接口类型
class ApiCategory(Base):
    __tablename__ = 'os_api_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=64), index=True, default='0')
    pid = Column(Integer, default=0)
    path = Column(String(length=64), default='0')
    level = Column(Integer, default=0)


# 接口列表
class ApiLists(Base):
    __tablename__ = 'os_api_lists'
    id = Column(Integer, primary_key=True)
    desc = Column(String(length=256), default='0')
    api_id = Column(Integer, index=True)
    href = Column(String(length=64), default='0')
    method = Column(String(length=8), default='0')
    request = Column(String(length=1024), default='0')
    response = Column(String(length=1024), default='0')
    response_string = Column(Text, default='0')
    remark = Column(String(length=255), default='0')
