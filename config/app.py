#!/usr/bin/python3

from pydantic import BaseSettings


class Settings(BaseSettings):
    # 数据库配置
    db_host: str = ''
    db_username: str = ''
    db_password: str = ''
    db_database: str = ''
    # redis 配置
    redis_host: str = ''
    redis_port: int = 3306
    redis_password: str = ''
    # 密钥
    secret_key: str = ''
    access_token_expire_minutes: int = 60
    token_algorithm: str = ''

    class Config:
        # 设置需要识别的 .env 文件
        env_file = '.env'
        # 设置字符编码
        env_file_encoding = 'utf-8'


settings = Settings()
