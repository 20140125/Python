#!/usr/bin/python3

from db.alchemyConnection import Session
from db.models import Users, to_json
from tools.logger import logger

session = Session()

"""
todo：获取单个用户
Parameter filters of db.crud.users.get
(filters: Any = None) -> Optional[dict]
"""


def get(filters=None):
    try:
        if filters is None:
            filters = []
        user = session.query(Users).filter(*filters).first()
        return to_json(user)
    except Exception as e:
        logger.error('get_user message：{}'.format(e))
        return None


"""
todo：获取用户列表
Parameter page, limit, filters of db.crud.users.lists
(page: {__sub__}, limit: {__mul__},filters: Any = None) -> Optional[Dict[str, List[dict]]]
"""


def lists(page, limit, filters=None):
    try:
        if filters is None:
            filters = []
        data = session.query(Users).filter(*filters).limit(limit).offset(limit * (page - 1))
        total = session.query(Users).filter(*filters).count()
        result = []
        for column in data:
            result.append(to_json(column))
        return {'items': result, 'total': total}
    except Exception as e:
        logger.error('user_list message：{}'.format(e))
        return None


"""
todo：获取所有用户
"""


def all_users():
    try:
        data = session.query(Users).all()
        result = []
        for column in data:
            result.append(to_json(column))
        return result
    except Exception as e:
        logger.error('all_users message：{}'.format(e))
        return None


"""
todo：保存用户
Parameter params of db.crud.users.save
params: {username, email, role_id, ip_address, status, created_at, updated_at, password, salt, remember_token, phone_number, avatar_url, uuid, char}
"""


def save(params):
    try:
        user = Users(
            username=params.username,
            email=params.email,
            role_id=params.role_id,
            ip_address=params.ip_address,
            status=params.status,
            created_at=params.created_at,
            updated_at=params.updated_at,
            password=params.password,
            salt=params.salt,
            remember_token=params.remember_token,
            phone_number=params.phone_number,
            avatar_url=params.avatar_url,
            uuid=params.uuid,
            char=params.char
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user.id
    except Exception as e:
        logger.error('save_user message：{}'.format(e))
        return None
