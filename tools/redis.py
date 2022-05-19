#!/usr/bin/python3

import redis

from config.app import Settings
from tools.logger import logger

'''
Redis模块
'''


class Redis:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None

    '''
    链接Redis数据库
    '''

    def set_connection(self):
        try:
            pool = redis.ConnectionPool(host=self.host, port=self.port, decode_responses=True)
            self.connection = redis.Redis(connection_pool=pool)
        except Exception as e:
            logger.error('Error set_connection message: {}'.format(e))

    '''
    数据存储 （Redis 字符串(String)）
    '''

    async def set_ex(self, key, time, value):
        try:
            self.set_connection()
            self.connection.setex(key, time, value)
        except Exception as e:
            logger.error('Error set_ex message: {}'.format(e))

    '''
    数据获取（Redis 字符串(String)）
    '''

    def get_value(self, key):
        try:
            self.set_connection()
            self.connection.get(key)
        except Exception as e:
            logger.error('Error get_value message: {}'.format(e))

    '''
    根据删除redis中的任意数据类型（string、hash、list、set、有序set）
    '''

    def delete_value(self, key):
        try:
            self.set_connection()
            self.connection.delete(key)
        except Exception as e:
            logger.error('Error delete_value message: {}'.format(e))

    '''
    数据存储（Redis 集合(Set)）
    '''

    def s_add(self, key, value):
        try:
            self.set_connection()
            self.connection.sadd(key, value)
        except Exception as e:
            logger.error('Error s_add message: {}'.format(e))

    '''
    数据获取（Redis 集合(Set)）
    '''

    def s_members(self, key):
        try:
            self.set_connection()
            self.connection.smembers(key)
        except Exception as e:
            logger.error('Error s_members message: {}'.format(e))

    '''
    数据删除（Redis 集合(Set)）
    '''

    def s_rem(self, key, value):
        try:
            self.set_connection()
            self.connection.srem(key, value)
        except Exception as e:
            logger.error('Error s_rem message: {}'.format(e))

    '''
    数据添加（列表头部 Redis 列表(List)）
    '''

    def l_push(self, key, value):
        try:
            self.set_connection()
            self.connection.lpush(key, value)
        except Exception as e:
            logger.error('Error l_push message: {}'.format(e))

    '''
    移除并返回列表的第一个元素（ Redis 列表(List)）
    '''

    def l_pop(self, key):
        try:
            self.set_connection()
            self.connection.lpop(key)
        except Exception as e:
            logger.error('Error l_pop message: {}'.format(e))

    '''
    数据添加（列表尾部 Redis 列表(List)）
    '''

    def r_push(self, key, value):
        try:
            self.set_connection()
            self.connection.rpush(key, value)
        except Exception as e:
            logger.error('Error r_push message: {}'.format(e))

    '''
    移除并返回列表的最末元素（ Redis 列表(List)）
    '''

    def r_pop(self, key):
        try:
            self.set_connection()
            self.connection.rpop(key)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))

    '''
    返回列表中指定区间内的元素（ Redis 列表(List)）
    '''

    def l_range(self, key, start, num):
        try:
            self.set_connection()
            self.connection.lrange(key, start, num)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))

    '''
    Redis hGetAll 命令用于返回哈希表中，所有的字段和值。（Redis 哈希 (hash)）
    '''

    def h_get_all(self, key):
        try:
            self.set_connection()
            self.connection.hgetall(key)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))

    '''
    命令用于为哈希表中的字段值加上指定增量值。（ Redis 哈希 (hash)）
    '''

    def h_inc_by(self, form, to, num):
        try:
            self.set_connection()
            self.connection.hincby(form, to, num)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))

    '''
    命令用于删除哈希表 key 中的一个或多个指定字段，不存在的字段将被忽略。（ Redis 哈希 (hash)）
    '''

    def h_del(self, form, to):
        try:
            self.set_connection()
            self.connection.hdel(form, to)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))

    '''
    获取所有的Key
    '''

    def keys(self, pattern):
        try:
            self.set_connection()
            self.connection.keys(pattern)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))

    '''
    命令用于获取列表长度。（ Redis 列表 (list)）
    '''

    def l_len(self, key):
        try:
            self.set_connection()
            self.connection.llen(key)
        except Exception as e:
            logger.error('Error r_pop message: {}'.format(e))


# 配置信息
config = Settings()
# redisClient初始化
redisClient = Redis(config.redis_host, config.redis_port)
