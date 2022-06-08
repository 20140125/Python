#!/usr/bin/python3

import redis

from config.app import Settings
from tools.logger import logger

"""
Redis模块
"""


class Redis:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None

    def set_connection(self):
        """
        todo:链接Redis数据库
        :return:
        """
        try:
            pool = redis.ConnectionPool(host=self.host, port=self.port, decode_responses=True)
            self.connection = redis.Redis(connection_pool=pool)
        except Exception as e:
            logger.error('Error set_connection message: {}'.format(e))

    async def set_ex(self, key, time, value):
        """
        todo: 数据存储 （Redis 字符串(String)）
        :param key:
        :param time:
        :param value:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.setex(key, time, value)
        except Exception as e:
            logger.error('Error set_ex message: {}'.format(e))

    async def get_value(self, key):
        """
        todo:数据获取（Redis 字符串(String)）
        :param key:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.get(key)
        except Exception as e:
            logger.error('Error get_value message: {}'.format(e))

    async def delete_value(self, key):
        """
        todo:根据删除redis中的任意数据类型（string、hash、list、set、有序set）
        :param key:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.delete(key)
        except Exception as e:
            logger.error('Error delete_value message: {}'.format(e))

    async def s_add(self, key, value):
        """
        todo:数据存储（Redis 集合(Set)）
        :param key:
        :param value:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.sadd(key, value)
        except Exception as e:
            logger.error('Error s_add message: {}'.format(e))

    async def s_members(self, key):
        """
        todo:数据获取（Redis 集合(Set)）
        :param key:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.smembers(key)
        except Exception as e:
            logger.error('Error s_members message: {}'.format(e))

    async def s_rem(self, key, value):
        """
        todo:数据删除（Redis 集合(Set)）
        :param key:
        :param value:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.srem(key, value)
        except Exception as e:
            logger.error('Error s_rem message: {}'.format(e))

    async def l_push(self, key, value):
        """
        todo: 数据添加（列表头部 Redis 列表(List)）
        :param key:
        :param value:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.lpush(key, value)
        except Exception as e:
            logger.error('Error l_push message: {}'.format(e))

    async def l_pop(self, key):
        """
        todo:移除并返回列表的第一个元素（ Redis 列表(List)）
        :param key:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.lpop(key)
        except Exception as e:
            logger.error('Error l_pop message: {}'.format(e))

    async def r_push(self, key, value):
        """
        todo:数据添加（列表尾部 Redis 列表(List)）
        :param key:
        :param value:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.rpush(key, value)
        except Exception as e:
            logger.error('Error r_push message: {}'.format(e))

    async def r_pop(self, key):
        """
        todo:移除并返回列表的最末元素（ Redis 列表(List)）
        :param key:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.rpop(key)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))

    async def l_range(self, key, start, num):
        """
        todo:返回列表中指定区间内的元素（ Redis 列表(List)）
        :param key:
        :param start:
        :param num:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.lrange(key, start, num)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))

    async def h_get_all(self, key):
        """
        todo:Redis hGetAll 命令用于返回哈希表中，所有的字段和值。（Redis 哈希 (hash)）
        :param key:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.hgetall(key)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))

    async def h_inc_by(self, form, to, num):
        """
        todo:命令用于为哈希表中的字段值加上指定增量值。（ Redis 哈希 (hash)）
        :param form:
        :param to:
        :param num:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.hincby(form, to, num)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))

    async def h_del(self, form, to):
        """
        todo:命令用于删除哈希表 key 中的一个或多个指定字段，不存在的字段将被忽略。（ Redis 哈希 (hash)）
        :param form:
        :param to:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.hdel(form, to)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))

    async def keys(self, pattern):
        """
        todo:获取所有的Key
        :param pattern:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.keys(pattern)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))

    async def l_len(self, key):
        """
        todo:命令用于获取列表长度。（ Redis 列表 (list)）
        :param key:
        :return:
        """
        try:
            self.set_connection()
            return self.connection.llen(key)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))


# 配置信息
config = Settings()
# redisClient初始化
redisClient = Redis(config.redis_host, config.redis_port)
