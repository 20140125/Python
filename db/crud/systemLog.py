#!/usr/bin/python3


from db.alchemyConnection import Session
from db.models import Log, to_json
from tools.logger import logger

session = Session()

"""
todo: 获取日志列表
Parameter page, limit, filters of db.crud.systemLog.lists
(page: {__sub__},limit: {__mul__},filters: Any = None) -> Coroutine[Any, Any, Optional[Dict[str, List[dict]]]]
"""


async def lists(page, limit, filters=None):
    try:
        if filters is None:
            filters = []
        data = session.query(Log).filter(*filters).limit(limit).offset(limit * (page - 1))
        total = session.query(Log).filter(*filters).count()
        result = []
        for column in data:
            result.append(to_json(column))
        return {'items': result, 'total': total}
    except Exception as e:
        logger.error('get_log_lists message：{}'.format(e))
        return None


"""
todo：保存系统日志
Parameter params of db.crud.systemLog.save 
params: {__getitem__}
"""


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


"""
todo：删除日志
Parameter filters of db.crud.systemLog.delete
(filters: Any = None) -> Optional[bool]
"""


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
