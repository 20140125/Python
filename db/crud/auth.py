#!/usr/bin/python3


from db.alchemyConnection import Session
from db.orm.auth import Auth

session = Session()


# 获取单个权限
def get_one_auth(filters=None):
    if filters is None:
        filters = []
    return session.query(Auth).filter(*filters).first().to_json()


# 获取权限列表
def get_auth_lists(page, limit, filters=None):
    if filters is None:
        filters = []
    data = session.query(Auth).filter(*filters).limit(limit).offset(limit * (page - 1))
    total = session.query(Auth).filter(*filters).count()
    result = []
    for comment in data:
        result.append(comment.to_json())
    return {'items': result, 'total': total}


# 保存权限
def save_auth(params):
    params.api = params.href.replace('/admin/', '/api/v1/')
    auth = Auth(name=params.name, href=params.href, status=params.status, pid=params.pid,
                api=params.api)
    session.add(auth)
    session.commit()
    session.refresh(auth)
    return auth.id


# 保存数据
def update_auth(params):
    auth = Auth(name=params.name, href=params.href, status=params.status, pid=params.pid,
                api=params.api, level=params.level, path=params.path)
    session.query(Auth).filter(Auth.id == params.id).update(auth)
    return session.commit()
