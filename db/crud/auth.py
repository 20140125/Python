#!/usr/bin/python3


from db.alchemyConnection import Session
from db import models
from tools.logger import logger

session = Session()

"""
todo: 获取单个权限
Parameter filters of db.crud.auth def get
(filters: Any = None) -> Optional[dict]
"""


def get(filters=None):
    try:
        if filters is None:
            filters = []
        auth = session.query(models.Auth).filter(*filters).first()
        return models.to_json(auth)
    except Exception as e:
        logger.error('get_one_auth message：{}'.format(e))
        return None


"""
todo: 获取权限列表
Parameter page, limit, filters of db.crud.auth def lists
(page: {__sub__},limit: {__mul__},filters: Any = None) -> Optional[Dict[str, List[dict]]]
"""


def lists(page, limit, filters=None):
    try:
        if filters is None:
            filters = []
        data = session.query(models.Auth).filter(*filters).limit(limit).offset(limit * (page - 1))
        total = session.query(models.Auth).filter(*filters).count()
        result = []
        for column in data:
            result.append(models.to_json(column))
        return {'items': result, 'total': total}
    except Exception as e:
        logger.error('get_auth_lists message：{}'.format(e))
        return None


"""
todo: 保存权限
Parameter params of db.crud.auth.save 
params: {api, href, name, status, pid}
"""


def save(auth):
    try:
        session.add(auth)
        session.commit()
        session.refresh(auth)
        return auth.id
    except Exception as e:
        logger.error('save_auth message：{}'.format(e))
        return None


"""
todo: 保存数据
Parameter params of db.crud.auth.update 
params: {id, path, pid, name, href, status, level, api}
"""


def update(params):
    try:
        item = session.query(models.Auth).filter(models.Auth.id == params.id).first()
        if 'path' in params.__dict__:
            item.path = params.path
        if 'path' in params.__dict__:
            item.id = params.id
        if 'pid' in params.__dict__:
            item.pid = params.pid
        if 'name' in params.__dict__:
            item.name = params.name
        if 'href' in params.__dict__:
            item.href = params.href
        if 'status' in params.__dict__:
            item.status = params.status
        if 'level' in params.__dict__:
            item.level = params.level
        if 'api' in params.__dict__:
            item.api = params.api
        session.commit()
        return True
    except Exception as e:
        logger.error('update_auth message：{}'.format(e))
        return None
