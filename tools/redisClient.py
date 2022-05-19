#!/usr/bin/python3
from typing import Union

from aioredis import Redis

from config.app import Settings
from tools.logger import logger


class RedisClient:

    def __init__(
            self,
            *,
            host: str,
            port: Union[int, 3306],
            password: Union[str, ''],
            db: Union[int, 1],
            socket_timeout: Union[int, 5]):
        # redis对象 在 @app.on_event("startup") 中连接创建
        self.redis_client = None
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.socket_timeout = socket_timeout

    # 设置链接
    def set_connection(self):
        try:
            self.redis_client = Redis.from_url(self.host)
        except Exception as e:
            logger.info(e)

    def set_value(self, key, value):
        try:
            self.set_connection()
            await self.redis_client.set(key, value)
        except Exception as e:
            logger.info(e)


# 获取配置信息
config = Settings()
# redis客服端链接
redis = RedisClient(host=config.redis_host)
