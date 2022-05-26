#!/usr/bin/python3


from db.alchemyConnection import Session
import db.models as models

session = Session()


# 获取单个权限
def get_one_auth(filters=None):
    if filters is None:
        filters = []
    return session.query(models.Auth).filter(*filters).first().to_json()


# 获取权限列表
def get_auth_lists(page, limit, filters=None):
    if filters is None:
        filters = []
    data = session.query(models.Auth).filter(*filters).limit(limit).offset(limit * (page - 1))
    total = session.query(models.Auth).filter(*filters).count()
    result = []
    for comment in data:
        result.append(comment.to_json())
    return {'items': result, 'total': total}


# 保存权限
def save_auth(params):
    params.api = params.href.replace('/admin/', '/api/v1/')
    item = models.Auth(name=params.name, href=params.href, status=params.status, pid=params.pid,
                       api=params.api)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item.id


# 保存数据
def update_auth(params):
    item = get_one_auth([models.Auth.id == params.id])
    for key, value in params:
        item[key] = value
    # item.path = params.path
    # item.id = params.id
    # item.pid = params.pid
    # item.name = params.name
    # item.href = params.href
    # item.status = params.status
    # item.level = params.level
    # item.api = params.api
    return session.query(models.Auth).filter([models.Auth.id == params.id]).update(params)
