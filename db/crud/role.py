#!/usr/bin/python3


from db.alchemyConnection import Session
from db.models import Role
from tools.logger import logger

session = Session()


# 获取角色
def get(filters=None):
    try:
        if filters is None:
            filters = []
        return session.query(Role).filter(*filters).first().to_json()
    except Exception as e:
        logger.error('get_one_role message：{}'.format(e))
        return None


# 获取角色列表
def lists(page, limit, filters=None):
    try:
        if filters is None:
            filters = []
        data = session.query(Role).filter(*filters).limit(limit).offset(limit * (page - 1))
        total = session.query(Role).filter(*filters).count()
        result = []
        for comment in data:
            result.append(comment.to_json())
        return {'items': result, 'total': total}
    except Exception as e:
        logger.error('get_one_role message：{}'.format(e))
        return None
