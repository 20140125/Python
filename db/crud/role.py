#!/usr/bin/python3


from db.alchemyConnection import Session
from db import models
from tools.logger import logger

session = Session()

"""
todo: 获取角色
Parameter filters of db.crud.role.get
(filters: Any = None) -> Optional[dict]
"""


def get(filters=None):
    try:
        if filters is None:
            filters = []
        return models.to_json(session.query(models.Role).filter(*filters).first())
    except Exception as e:
        logger.error('get_one_role message：{}'.format(e))
        return None


"""
todo：获取角色列表
Parameter page, limit, filters of db.crud.role.get
(page: {__sub__},limit: {__mul__},filters: Any = None) -> Optional[Dict[str, List[dict]]]
"""


def lists(page, limit, filters=None):
    try:
        if filters is None:
            filters = []
        data = session.query(models.Role).filter(*filters).limit(limit).offset(limit * (page - 1))
        total = session.query(models.Role).filter(*filters).count()
        result = []
        for column in data:
            result.append(models.to_json(column))
        return {'items': result, 'total': total}
    except Exception as e:
        logger.error('get_one_role message：{}'.format(e))
        return None
