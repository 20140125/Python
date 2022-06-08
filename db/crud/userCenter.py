#!/usr/bin/python3

from db.alchemyConnection import db
from db import models
from tools.logger import logger


def get(filters=None):
    """
    todo：获取单个用户信息
    :param filters:
    :return:
    """
    try:
        if filters is None:
            filters = []
        return models.to_json(db.query(models.UsersCenter).filter(*filters).first())
    except Exception as e:
        logger.error('get_user_center message：{}'.format(e))
        return None


def save(userCenter):
    """
    todo：保存用户信息
    :param userCenter:
    :return:
    """
    try:
        db.add(userCenter)
        db.commit()
        db.refresh(userCenter)
        return userCenter.id
    except Exception as e:
        logger.error('save_user_center message：{}'.format(e))
        return None


def update(userCenter, filters):
    """
    todo：更新用户信息
    :param userCenter:
    :param filters:
    :return:
    """
    try:
        item = db.query(models.UsersCenter).filter(*filters).first()
        if 'u_name' in userCenter.__dict__:
            item.u_name = userCenter.u_name
        if 'tags' in userCenter.__dict__:
            item.u_tags = userCenter.tags
        if 'local' in userCenter.__dict__:
            item.local = userCenter.local
        if 'ip_address' in userCenter.__dict__:
            item.ip_address = userCenter.ip_address
        if 'user_status' in userCenter.__dict__:
            item.user_status = userCenter.user_status
        if 'notice_status' in userCenter.__dict__:
            item.notice_status = userCenter.notice_status
        if 'desc' in userCenter.__dict__:
            item.desc = userCenter.desc
        if 'token' in userCenter.__dict__:
            item.token = userCenter.token
        db.commit()
        return True
    except Exception as e:
        logger.error('update_user_center message：{}'.format(e))
        return None
