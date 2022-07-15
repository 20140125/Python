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
