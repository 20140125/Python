#!/usr/bin/python3

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SystemLog(Base):
    __tablename__ = 'os_system_log'

    id = Column(Integer, primary_key=True)
    username = Column(String(length=32), index=True)
    url = Column(String(length=64))
    ip_address = Column(String(length=32), index=True)
    log = Column(Text)
    created_at = Column(Integer)
    day = Column(String(length=16))
    local = Column(String(length=128))

    def to_json(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
