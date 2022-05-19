#!/usr/bin/python3

import pymysql
from pymysql import cursors

from config.app import Settings
from tools.logger import logger

"""
数据库模块
"""


class MySQLdb:

    # MySQL实例化
    def __init__(self, *, host, user, password, database):
        self.cursor = None
        self.connection = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    # 数据库链接
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
            logger.info("Error connecting message: {}".format(e))

    # 关闭数据库链接
    def cloe_connection(self):
        self.connection.close()
        self.cursor.close()

    # 获取一条结构集
    def get_one(self, sql, value):
        result = None
        try:
            self.set_connection()
            self.cursor.execute(sql, value)
            logger.info(sql)
            result = self.cursor.fetchone()
            self.cloe_connection()
        except Exception as e:
            logger.info('Error fetchone message: {}'.format(e))
        return result

    # 获取多条结果集
    def get_lists(self, sql, values):
        result = None
        try:
            self.set_connection()
            self.cursor.execute(sql, values)
            logger.info(sql)
            result = self.cursor.fetchall()
            self.cloe_connection()
        except Exception as e:
            logger.info('Error fetchall message: {}'.format(e))
        return result

    # 插入/修改一条记录
    def insert_one(self, sql, value):
        result = False
        try:
            self.set_connection()
            self.cursor.execute(sql, value)
            logger.info(sql)
            self.connection.commit()
            result = self.cursor.rowcount == 1
            self.cloe_connection()
        except Exception as e:
            logger.info('Error insertOne message: {}'.format(e))
        return result

    # 插入/修改多条记录
    def insert_more(self, sql, values):
        result = False
        try:
            self.set_connection()
            self.cursor.execute(sql, values)
            logger.info(sql)
            self.connection.commit()
            result = self.cursor.rowcount == len(values)
            self.cloe_connection()
        except Exception as e:
            logger.info('Error insertMore message: {}'.format(e))
        return result


# 获取配置信息
config = Settings()

# 数据库实例化
MySQLdb = MySQLdb(host=config.db_host, user=config.db_username, password=config.db_password, database=config.db_database)
