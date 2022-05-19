#!/usr/bin/python3

from pydantic import BaseSettings


class Settings(BaseSettings):
    # 数据库配置
    db_host: str
    db_username: str
    db_password: str
    db_database: str
    # redis 配置
    redis_host: str
    redis_port: int
    redis_password: str

    class Config:
        # 设置需要识别的 .env 文件
        env_file = '.env'
        # 设置字符编码
        env_file_encoding = 'utf-8'


settings = Settings()
