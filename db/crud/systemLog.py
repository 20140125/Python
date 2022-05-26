#!/usr/bin/python3


from db.alchemyConnection import Session
import db.models as models

session = Session()


# 获取日志列表
async def get_log_lists(page, limit, filters=None):
    if filters is None:
        filters = []
    items = session.query(models.Log).filter(*filters).limit(limit).offset(limit * (page - 1)).to_json()
    total = session.query(models.Log).filter(*filters).count()
    result = []
    for comment in items:
        result.append(comment.to_json())
    return {'items': result, 'total': total}


# 保存系统日志
def insert_log(params):
    log = models.Log(username=params['username'], url=params['url'], ip_address=params['ip_address'], log=params['log'],
                     created_at=params['created_at'], day=params['day'])
    session.add(log)
    session.commit()
    session.refresh(log)
    return log.id


# 删除日志
def delete_log(params):
    session.query(models.Log).filter(models.Log.id == params.id).delete()
    return session.commit()
