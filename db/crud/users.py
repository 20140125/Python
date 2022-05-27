#!/usr/bin/python3


from db.alchemyConnection import Session
from db.models import Users

session = Session()


# 获取单个用户
def get_one_user(filters=None):
    if filters is None:
        filters = []
    return session.query(Users).filter(*filters).first().to_json()


# 获取用户列表
def get_user_lists(page, limit, filters=None):
    if filters is None:
        filters = []
    data = session.query(Users).filter(*filters).limit(limit).offset(limit * (page - 1))
    total = session.query(Users).filter(*filters).count()
    result = []
    for comment in data:
        result.append(comment.to_json())
    return {'items': result, 'total': total}
