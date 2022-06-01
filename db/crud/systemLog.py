#!/usr/bin/python3


from db.alchemyConnection import db
from db import models
from tools.logger import logger

"""
todo: 获取日志列表
Parameter page, limit, filters of db.crud.systemLog.lists
(page: {__sub__},limit: {__mul__},filters: Any = None) -> Coroutine[Any, Any, Optional[Dict[str, List[dict]]]]
"""


def lists(page, limit, filters=None):
    try:
        if filters is None:
            filters = []
        data = db.query(models.Log).filter(*filters).order_by(models.Log.id.desc()).limit(limit).offset(limit * (page - 1))
        total = db.query(models.Log).filter(*filters).count()
        result = []
        for column in data:
            result.append(models.to_json(column))
        return {'items': result, 'total': total}
    except Exception as e:
        logger.error('get_log_lists message：{}'.format(e))
        return None


"""
todo：保存系统日志
Parameter params of db.crud.systemLog.save 
params: {__getitem__}
"""


def save(log):
    try:
        db.add(log)
        db.commit()
        db.refresh(log)
        return log.id
    except Exception as e:
        logger.error('insert_log message：{}'.format(e))
        return None


"""
todo：删除日志
Parameter filters of db.crud.systemLog.delete
(filters: Any = None) -> Optional[bool]
"""


def delete(filters=None):
    try:
        if filters is None:
            filters = []
        db.query(models.Log).filter(*filters).delete()
        db.commit()
        return True
    except Exception as e:
        logger.error('delete_log message：{}'.format(e))
        return None
