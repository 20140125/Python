#!/usr/bin/python3


from db.AlchemyConnection import Session
from db.orm.SystemLog import SystemLog


session = Session()


async def get_log_lists(filters, page, limit):
    return await session.query(SystemLog).filter(*filters).limit(limit).offset(limit * (page - 1)).to_json()

# 保存系统日志
def insert_log(params):
    log = SystemLog(
        username=params['username'],
        url=params['url'],
        ip_address=params['ip_address'],
        log=params['log'],
        created_at=params['created_at'],
        day=params['day']
    )
    session.add(log)
    session.commit()
    return log.id
