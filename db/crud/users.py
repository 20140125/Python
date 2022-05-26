#!/usr/bin/python3


from db.alchemyConnection import Session
import db.models as models

# session = Session()


# 获取单个用户
def get_one_user(db: Session, filters=None):
    if filters is None:
        filters = []
    return db.query(models.Users).filter(*filters).first().to_json()


# 获取用户列表
def get_user_lists(db: Session, page, limit, filters=None):
    if filters is None:
        filters = []
    data = db.query(models.Users).filter(*filters).limit(limit).offset(limit * (page - 1))
    total = db.query(models.Users).filter(*filters).count()
    result = []
    for comment in data:
        result.append(comment.to_json())
    return {'items': result, 'total': total}
