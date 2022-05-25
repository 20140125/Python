#!/usr/bin/python3


from db.AlchemyConnection import Session
from db.orm.Auth import Auth

session = Session()


# 获取单个权限
def get_one_auth(filters = []):
    return session.query(Auth).filter(*filters).first().to_json()


# 获取权限列表
def get_auth_lists(page, limit, filters = []):
    data = session.query(Auth).filter(*filters).limit(limit).offset(limit * (page - 1))
    total = session.query(Auth).filter(*filters).count()
    result = []
    for comment in data:
        result.append(comment.to_json())
    return {'items': result, 'total': total}

