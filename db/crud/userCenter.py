#!/usr/bin/python3

from db.alchemyConnection import Session
from db import models
from tools.logger import logger

session = Session()

"""
todo：获取单个用户信息
Parameter filters of db.crud.userCenter.get
(filters: Any = None) -> Optional[dict]
"""


def get(filters=None):
    try:
        if filters is None:
            filters = []
        return models.to_json(session.query(models.UsersCenter).filter(*filters).first())
    except Exception as e:
        logger.error('get_user_center message：{}'.format(e))
        return None


"""
todo：保存用户信息
Parameter user of db.crud.userCenter.save
user: db.models.UsersCenter
"""


def save(userCenter):
    try:
        session.add(userCenter)
        session.commit()
        session.refresh(userCenter)
        return userCenter.id
    except Exception as e:
        logger.error('save_user message：{}'.format(e))
        return None


"""
todo：更新用户信息
Parameter user of db.crud.userCenter.update
(user: db.models.UsersCenter)
return Optional[bool]
"""


def update(userCenter, filters):
    try:
        item = session.query(models.UsersCenter).filter(*filters).first()
        if 'u_name' in userCenter:
            item.u_name = userCenter.u_name
        if 'tags' in userCenter:
            item.u_tags = userCenter.tags
        if 'local' in userCenter:
            item.local = userCenter.local
        if 'ip_address' in userCenter:
            item.ip_address = userCenter.ip_address
        if 'user_status' in userCenter:
            item.user_status = userCenter.user_status
        if 'notice_status' in userCenter:
            item.notice_status = userCenter.notice_status
        if 'desc' in userCenter:
            item.desc = userCenter.desc
        if 'token' in userCenter:
            item.token = userCenter.token
        session.commit()
        return True
    except Exception as e:
        logger.error('save_user message：{}'.format(e))
        return None
