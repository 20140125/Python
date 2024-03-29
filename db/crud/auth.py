#!/usr/bin/python3


from db.alchemyConnection import db
from db import models
from tools.logger import logger


def get(filters=None):
    """
    todo: 获取单个权限
    :param filters:
    :return:
    """
    try:
        if filters is None:
            filters = []
        auth = db.query(models.Auth).filter(*filters).first()
        return models.to_json(auth)
    except Exception as e:
        logger.error('get_one_auth message：{}'.format(e))
        return None


def lists(page, limit, filters=None):
    """
    todo: 获取权限列表
    :param page:
    :param limit:
    :param filters:
    :return:
    """
    try:
        if filters is None:
            filters = []
        data = db.query(models.Auth).filter(*filters).order_by(models.Auth.path.desc()).limit(limit).offset(
            limit * (page - 1))
        total = db.query(models.Auth).filter(*filters).count()
        result = []
        for column in data:
            result.append(models.to_json(column))
        return {'items': result, 'total': total}
    except Exception as e:
        logger.error('get_auth_lists message：{}'.format(e))
        return None


def all_users():
    """
    todo：获取所有权限
    :return:
    """
    try:
        data = db.query(models.Auth).order_by(models.Auth.path.desc()).all()
        result = []
        for column in data:
            result.append(models.to_json(column))
        return result
    except Exception as e:
        logger.error('all_users message：{}'.format(e))
        return None


def save(auth):
    """
    todo: 保存权限
    :param auth:
    :return:
    """
    try:
        db.add(auth)
        db.commit()
        db.refresh(auth)
        return auth.id
    except Exception as e:
        db.rollback()
        logger.error('save_auth message：{}'.format(e))
        return None


def update(params):
    """
    todo: 更新权限
    :param params:
    :return:
    """
    try:
        item = db.query(models.Auth).filter(models.Auth.id == params.id).first()
        if 'path' in params.__dict__:
            item.path = params.path
        if 'path' in params.__dict__:
            item.id = params.id
        if 'pid' in params.__dict__:
            item.pid = params.pid
        if 'name' in params.__dict__:
            item.name = params.name
        if 'href' in params.__dict__:
            item.href = params.href
        if 'status' in params.__dict__:
            item.status = params.status
        if 'level' in params.__dict__:
            item.level = params.level
        if 'api' in params.__dict__:
            item.api = params.api
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error('update_auth message：{}'.format(e))
        return None
