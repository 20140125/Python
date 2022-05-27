#!/usr/bin/python3


from db.alchemyConnection import Session
import db.models as models

session = Session()


# 获取角色
def get_one_role(filters=None):
    if filters is None:
        filters = []
    return session.query(models.Role).filter(*filters).first().to_json()


# 获取角色列表
def get_role_lists(page, limit, filters=None):
    if filters is None:
        filters = []
    data = session.query(models.Role).filter(*filters).limit(limit).offset(limit * (page - 1))
    total = session.query(models.Role).filter(*filters).count()
    result = []
    for comment in data:
        result.append(comment.to_json())
    return {'items': result, 'total': total}
