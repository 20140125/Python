#!/usr/bin/python3


from db.alchemyConnection import Session
import db.models as models


# 获取角色
def get_one_role(db: Session, filters=None):
    if filters is None:
        filters = []
    return db.query(models.Role).filter(*filters).first().to_json()


# 获取角色列表
def get_role_lists(db: Session, page, limit, filters=None):
    if filters is None:
        filters = []
    data = db.query(models.Role).filter(*filters).limit(limit).offset(limit * (page - 1))
    total = db.query(models.Role).filter(*filters).count()
    result = []
    for comment in data:
        result.append(comment.to_json())
    return {'items': result, 'total': total}
