#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Role(Base):
    __tablename__ = 'os_role'

    id = Column(Integer, primary_key=True)
    role_name = Column(String(length=64), index=True)
    auth_ids = Column(Text)
    auth_api = Column(Text)
    status = Column(Integer)
    created_at = Column(Integer)
    updated_at = Column(Integer)

    def to_json(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
