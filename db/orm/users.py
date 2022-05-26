#!/usr/bin/python3

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'os_users'

    id = Column(Integer, primary_key=True)
    username = Column(String(length=64))
    email = Column(String(length=32))
    role_id = Column(Integer())
    ip_address = Column(String(length=32))
    status = Column(Integer())
    created_at = Column(Integer())
    updated_at = Column(Integer())
    password = Column(String(length=32))
    salt = Column(String(length=8))
    remember_token = Column(String(length=1000))
    phone_number = Column(String(length=11))
    avatar_url = Column(String(length=512))
    uuid = Column(String(length=128))
    char = Column(String(length=1))

    def to_json(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
