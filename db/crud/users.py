#!/usr/bin/python3
import time

from db.alchemyConnection import db
from db import models
from tools.logger import logger


def get(filters=None):
    """
    todo：获取单个用户
    :param filters:
    :return:
    """
    try:
        if filters is None:
            filters = []
        return models.to_json(db.query(models.Users).filter(*filters).first())
    except Exception as e:
        logger.error('get_user message：{}'.format(e))
        return None


def lists(page, limit, filters=None):
    """
    todo：获取用户列表
    :param page:
    :param limit:
    :param filters:
    :return:
    """
    try:
        if filters is None:
            filters = []
        data = db.query(models.Users).filter(*filters).order_by(models.Users.updated_at.desc()).limit(limit).offset(
            limit * (page - 1))
        total = db.query(models.Users).filter(*filters).count()
        result = []
        for column in data:
            result.append(models.to_json(column))
        return {'items': result, 'total': total}
    except Exception as e:
        logger.error('user_list message：{}'.format(e))
        return None


def all_users():
    """
    todo：获取所有用户
    :return:
    """
    try:
        data = db.query(models.Users).all()
        result = []
        for column in data:
            result.append(models.to_json(column))
        return result
    except Exception as e:
        logger.error('all_users message：{}'.format(e))
        return None


def save(user):
    """
    todo：保存用户
    :param user:
    :return:
    """
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user.id
    except Exception as e:
        db.rollback()
        logger.error('save_user message：{}'.format(e))
        return None


def update(user, filters):
    """
    todo：更新用户
    :param user:
    :param filters:
    :return:
    """
    try:
        item = db.query(models.Users).filter(*filters).first()
        item.updated_at = int(time.time())
        if 'uuid' in user.__dict__:
            item.uuid = '{}{}'.format(user.uuid, item.id)
        if 'status' in user.__dict__:
            item.status = user.status
        if 'username' in user.__dict__:
            item.username = user.username
        if 'password' in user.__dict__:
            item.password = user.password
        if 'remember_token' in user.__dict__:
            item.remember_token = user.remember_token
        if 'salt' in user.__dict__:
            item.salt = user.salt
        if 'avatar_url' in user.__dict__:
            item.avatar_url = user.avatar_url
        if 'role_id' in user.__dict__:
            item.role_id = user.role_id
        if 'phone_number' in user.__dict__:
            item.phone_number = user.phone_number
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error('update_user message：{}'.format(e))
        return None
