#!/usr/bin/python3
import random

from db.alchemyConnection import db
from db import models
from tools.logger import logger


def lists(page, limit, filters=None):
    """
    todo:获取图片列表
    :param filters:
    :param page:
    :param limit:
    :return:
    """
    try:
        total = db.query(models.Image).count()
        if filters is None:
            filters = [models.Image.id >= random.randint(1, total - 100)]
        data = db.query(models.Image).filter(*filters).limit(limit).offset(limit * (page - 1))
        result = []
        for column in data:
            result.append(models.to_json(column))
        return {'items': result, 'total': total}
    except Exception as e:
        logger.error('get_image_lists message：{}'.format(e))
        return None


def get(filters=None):
    """
    todo：获取单张用户
    :param filters:
    :return:
    """
    try:
        if filters is None:
            filters = []
        return models.to_json(db.query(models.Image).filter(*filters).first())
    except Exception as e:
        logger.error('get_image message：{}'.format(e))
        return None


def save(image):
    """
      todo：保存图片
      :param image:
      :return:
      """
    try:
        db.add(image)
        db.commit()
        db.refresh(image)
        return image.id
    except Exception as e:
        db.rollback()
        logger.error('save_image message：{}'.format(e))
        return None


def update(image, filters):
    """
    todo:保存图片
    :param image:
    :param filters:
    :return:
    """
    try:
        item = db.query(models.Image).filter(*filters).first()
        if 'href' in image.__dict__:
            item.href = image.href
        if 'name' in image.__dict__:
            item.name = image.name
        if 'width' in image.__dict__:
            item.width = image.width
        if 'height' in image.__dict__:
            item.height = image.height
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error('update_image message：{}'.format(e))
        return None
