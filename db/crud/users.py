#!/usr/bin/python3
import time

from db.alchemyConnection import Session
from db import models
from tools.logger import logger

session = Session()

"""
todo：获取单个用户
Parameter filters of db.crud.users.get
(filters: Any = None) -> Optional[dict]
"""


def get(filters=None):
    try:
        if filters is None:
            filters = []
        return models.to_json(session.query(models.Users).filter(*filters).first())
    except Exception as e:
        logger.error('get_user message：{}'.format(e))
        return None


"""
todo：获取用户列表
Parameter page, limit, filters of db.crud.users.lists
(page: {__sub__}, limit: {__mul__},filters: Any = None) -> Optional[Dict[str, List[dict]]]
"""


def lists(page, limit, filters=None):
    try:
        if filters is None:
            filters = []
        data = session.query(models.Users).filter(*filters).limit(limit).offset(limit * (page - 1))
        total = session.query(models.Users).filter(*filters).count()
        result = []
        for column in data:
            result.append(models.to_json(column))
        return {'items': result, 'total': total}
    except Exception as e:
        logger.error('user_list message：{}'.format(e))
        return None


"""
todo：获取所有用户
"""


def all_users():
    try:
        data = session.query(models.Users).all()
        result = []
        for column in data:
            result.append(models.to_json(column))
        return result
    except Exception as e:
        logger.error('all_users message：{}'.format(e))
        return None


"""
todo：保存用户
Parameter user of db.crud.users.save
user: db.models.Users
"""


def save(user):
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user.id
    except Exception as e:
        logger.error('save_user message：{}'.format(e))
        return None


"""
todo：更新用户
Parameter user of db.crud.users.update
(user: db.models.Users)
return Optional[bool]
"""


def update(user):
    try:
        item = session.query(models.Users).filter(models.Users.id == user.id).first()
        item.uuid = user.uuid + '{}'.format(user.id)
        item.updated_at = int(time.time()),
        if 'status' in user:
            item.status = user.status
        if 'username' in user:
            item.username = user.username
        if 'password' in user:
            item.password = user.password
        if 'remember_token' in user:
            item.remember_token = user.remember_token
        if 'salt' in user:
            item.salt = user.salt
        if 'avatar_url' in user:
            item.avatar_url = user.avatar_url
        if 'role_id' in user:
            item.role_id = user.role_id
        if 'phone_number' in user:
            item.phone_number = user.phone_number
        session.commit()
        return True
    except Exception as e:
        logger.error('save_user message：{}'.format(e))
        return None
