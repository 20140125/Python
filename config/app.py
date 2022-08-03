#!/usr/bin/python3

from pydantic import BaseSettings

"""
todo：系统配置
config.app
class Settings(BaseSettings)
"""


class Settings(BaseSettings):
    # 系统配置
    app_name: str = ''
    app_username: str = ''
    app_email: str = ''
    app_host: str = ''
    app_refresh_login_time: int = 3600
    set_redis_timeout: int = 600
    users_cache_key: str = ''
    default_uuid: str = ''
    default_password: str = ''

    # 数据库配置
    db_connection: str = 'mysql'
    db_host: str = '127.0.0.1'
    db_port: int = 3306
    db_database: str = 'longer'
    db_username: str = 'root'
    db_password: str = '123456789'
    db_debug: bool = True

    # redis 配置
    redis_host: str = '127.0.0.1'
    redis_port: int = 3306
    redis_password: str = ''

    # 密钥
    secret_key: str = ''
    access_token_expire_minutes: int = 60
    token_algorithm: str = ''

    # 邮箱
    mail_driver: str = ''
    mail_host: str = ''
    mail_port: int = 465
    mail_username: str = ''
    mail_password: str = ''
    mail_encryption: str = ''
    mail_from_address: str = ''
    mail_from_name: str = ''

    # 高德地图
    a_map_key: str = ''

    # 小程序
    mini_program_app_key: str = ''
    mini_program_app_secret: str = ''

    # 公众号
    cen_key: str = ''
    cen_app_secret: str = ''
    encode_as_key: str = ''
    cen_token: str = ''

    # Github授权登录
    github_token: str = ''
    github_appid: str = ''
    github_app_secret: str = ''
    github_redirect_uri: str = ''

    # 微博授权登录
    weibo_appid: str = ''
    weibo_app_secret: str = ''
    weibo_redirect_uri: str = ''

    # 码云授权登录
    gitee_appid: str = ''
    gitee_app_secret: str = ''
    gitee_access_token: str = ''
    gitee_redirect_uri: str = ''

    # QQ授权登录
    qq_appid: str = ''
    qq_app_secret: str = ''
    qq_redirect_uri: str = ''

    # Baidu授权登录
    baidu_id: str = ''
    baidu_appid: str = ''
    baidu_app_secret: str = ''
    baidu_redirect_uri: str = ''

    # 百度智能云识别
    baidu_image_id: str = ''
    baidu_image_appid: str = ''
    baidu_image_secret: str = ''

    # 阿里云授权登录
    a_li_yun_appid: str = ''
    a_li_yun_app_secret: str = ''

    # osChina授权登录
    os_china_appid: str = ''
    os_china_app_secret: str = ''
    os_china_redirect_uri: str = ''

    class Config:
        # 设置需要识别的 .env 文件
        env_file = '.env'
        # 设置字符编码
        env_file_encoding = 'utf-8'


settings = Settings()
