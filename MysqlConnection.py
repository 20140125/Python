#!/usr/bin/python3

import mysql.connector
from logger import logger

"""
数据库模块
"""


class MySQLdb:

    # MySQL实例化
    def __init__(self, host, user, passwd, database):
        self.cursor = None
        self.connection = None
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database

    # 数据库链接
    def setConnection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host, user=self.user, passwd=self.passwd, database=self.database
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except Exception as e:
            logger.info("Error connecting message: {}".format(e))

    # 关闭数据库链接
    def cloeConnection(self):
        self.connection.close()
        self.cursor.close()

    # 获取一条结构集
    def getOne(self, sql, value):
        result = None
        try:
            self.setConnection()
            self.cursor.execute(sql, value)
            logger.info(sql)
            result = self.cursor.fetchone()
            self.cloeConnection()
        except Exception as e:
            logger.info('Error fetchone message: {}'.format(e))
        return result

    # 获取多条结果集
    def getLists(self, sql):
        result = None
        try:
            self.setConnection()
            self.cursor.execute(sql)
            logger.info(sql)
            result = self.cursor.fetchall()
            self.cloeConnection()
        except Exception as e:
            logger.info('Error fetchall message: {}'.format(e))
        return result

    # 插入/修改一条记录
    def insertOne(self, sql, value):
        result = False
        try:
            self.setConnection()
            self.cursor.execute(sql, value)
            logger.info(sql)
            self.connection.commit()
            result = self.cursor.rowcount == 1
            self.cloeConnection()
        except Exception as e:
            logger.info('Error insertOne message: {}'.format(e))
        return result

    # 插入/修改多条记录
    def insertMore(self, sql, values):
        result = False
        try:
            self.setConnection()
            self.cursor.execute(sql, values)
            logger.info(sql)
            self.connection.commit()
            result = self.cursor.rowcount == len(values)
            self.cloeConnection()
        except Exception as e:
            logger.info('Error insertMore message: {}'.format(e))
        return result
