#!/usr/bin/python3


from db.alchemyConnection import db
from db import models
from tools.logger import logger


def lists(page, limit, filters=None):
    """
    todo: 获取日志列表
    :param page:
    :param limit:
    :param filters:
    :return:
    """
    try:
        if filters is None:
            filters = []
        data = db.query(models.Log).filter(*filters).order_by(models.Log.id.desc()).limit(limit).offset(
            limit * (page - 1))
        total = db.query(models.Log).filter(*filters).count()
        result = []
        for column in data:
            result.append(models.to_json(column))
        return {'items': result, 'total': total}
    except Exception as e:
        logger.error('get_log_lists message：{}'.format(e))
        return None


def save(log):
    """
    todo：保存系统日志
    :param log:
    :return:
    """
    try:
        db.add(log)
        db.commit()
        return log
    except Exception as e:
        db.rollback()
        logger.error('insert_log message：{}'.format(e))
        return None


def delete(filters=None):
    """
    todo：删除日志
    :param filters:
    :return:
    """
    try:
        if filters is None:
            filters = []
        db.query(models.Log).filter(*filters).delete()
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error('delete_log message：{}'.format(e))
        return None
