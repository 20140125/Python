#!/usr/bin/python3

import pymysql
from pymysql import cursors

from config.app import Settings
from tools.logger import logger

'''
数据库模块
'''


class MySQLdb:

    # MySQL实例化
    def __init__(self, *, host, user, password, database):
        self.cursor = None
        self.connection = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    '''
    数据库链接
    '''

    def set_connection(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            logger.error('Error connecting message: {}'.format(e))

    '''
    关闭数据库链接
    '''

    def cloe_connection(self):
        self.connection.close()
        self.cursor.close()

    '''
    获取一条结构集
    '''

    async def get_one(self, sql, value):
        result = None
        try:
            self.set_connection()
            await self.cursor.execute(sql, value)
            logger.debug(sql)
            result = await self.cursor.fetchone()
            self.cloe_connection()
        except Exception as e:
            logger.error('Error fetchone message: {}'.format(e))
        return result

    '''
    获取多条结果集
    '''

    async def get_lists(self, sql, values):
        result = None
        try:
            self.set_connection()
            await self.cursor.execute(sql, values)
            logger.debug(sql)
            result = await self.cursor.fetchall()
            self.cloe_connection()
        except Exception as e:
            logger.error('Error fetchall message: {}'.format(e))
        return result

    '''
    插入/修改一条记录
    '''

    async def update_one(self, sql, value):
        result = False
        try:
            self.set_connection()
            await self.cursor.execute(sql, value)
            logger.debug(sql)
            self.connection.commit()
            result = self.cursor.lastrowid
            self.cloe_connection()
        except Exception as e:
            logger.error('Error update_one message: {}'.format(e))
        return result

    '''
    插入/修改多条记录
    '''

    async def update_more(self, sql, values):
        result = False
        try:
            self.set_connection()
            await self.cursor.execute(sql, values)
            logger.debug(sql)
            self.connection.commit()
            result = self.cursor.rowcount == len(values)
            self.cloe_connection()
        except Exception as e:
            logger.error('Error update_more message: {}'.format(e))
        return result


# 获取配置信息
config = Settings()

# 数据库实例化
MySQLdb = MySQLdb(
    host=config.db_host,
    user=config.db_username,
    password=config.db_password,
    database=config.db_database
)
