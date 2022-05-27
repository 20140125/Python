#!/usr/bin/python3


from db.alchemyConnection import Session
from db.models import Auth
from tools.logger import logger

session = Session()


# 获取单个权限
def get(filters=None):
    try:
        if filters is None:
            filters = []
        return session.query(Auth).filter(*filters).first().to_json()
    except Exception as e:
        logger.error('get_one_auth message：{}'.format(e))
        return None


# 获取权限列表
def lists(page, limit, filters=None):
    try:
        if filters is None:
            filters = []
        data = session.query(Auth).filter(*filters).limit(limit).offset(limit * (page - 1))
        total = session.query(Auth).filter(*filters).count()
        result = []
        for comment in data:
            result.append(comment.to_json())
        return {'items': result, 'total': total}
    except Exception as e:
        logger.error('get_auth_lists message：{}'.format(e))
        return None


# 保存权限
def save(params):
    try:
        params.api = params.href.replace('/admin/', '/api/v1/')
        item = Auth(
            name=params.name,
            href=params.href,
            status=params.status,
            pid=params.pid,
            api=params.api
        )
        session.add(item)
        session.commit()
        session.refresh(item)
        return item.id
    except Exception as e:
        logger.error('save_auth message：{}'.format(e))
        return None


# 保存数据
def update(params):
    try:
        item = session.query(Auth).filter(Auth.id == params.id).first()
        item.path = params.path
        item.id = params.id
        item.pid = params.pid
        item.name = params.name
        item.href = params.href
        item.status = params.status
        item.level = params.level
        item.api = params.api
        session.commit()
        return True
    except Exception as e:
        logger.error('update_auth message：{}'.format(e))
        return None
