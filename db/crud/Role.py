#!/usr/bin/python3


from db.AlchemyConnection import Session
from db.orm.Role import Role

session = Session()


# 获取角色
def get_one_role(filters = []):
    return session.query(Role).filter(*filters).first().to_json()


# 获取角色列表
def get_role_lists(page, limit, filters = []):
    data = session.query(Role).filter(*filters).limit(limit).offset(limit * (page - 1))
    total = session.query(Role).filter(*filters).count()
    result = []
    for comment in data:
        result.append(comment.to_json())
    return {'items': result, 'total': total}
