#!/usr/bin/python3

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class auth(Base):
    __tablename__ = 'os_auth'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    href = Column(String(length=255))
    api = Column(String(length=255))
    pid = Column(Integer, index=True)
    path = Column(String(length=255))
    level = Column(Integer)
    status = Column(Integer)

    def to_json(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
