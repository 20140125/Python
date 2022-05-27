#!/usr/bin/python3


from db.alchemyConnection import Session
from db.models import Log
from tools.logger import logger

session = Session()


# 获取日志列表
async def lists(page, limit, filters=None):
    try:
        if filters is None:
            filters = []
        items = session.query(Log).filter(*filters).limit(limit).offset(limit * (page - 1)).to_json()
        total = session.query(Log).filter(*filters).count()
        result = []
        for comment in items:
            result.append(comment.to_json())
        return {'items': result, 'total': total}
    except Exception as e:
        logger.error('get_log_lists message：{}'.format(e))
        return None


# 保存系统日志
def save(params):
    try:
        log = Log(
            username=params['username'],
            url=params['url'],
            ip_address=params['ip_address'],
            log=params['log'],
            created_at=params['created_at'],
            day=params['day']
        )
        session.add(log)
        session.commit()
        session.refresh(log)
        return log.id
    except Exception as e:
        logger.error('insert_log message：{}'.format(e))
        return None


# 删除日志
def delete(filters=None):
    try:
        if filters is None:
            filters = []
        session.query(Log).filter(*filters).delete()
        session.commit()
        return True
    except Exception as e:
        logger.error('delete_log message：{}'.format(e))
        return None
