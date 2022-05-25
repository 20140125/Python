#!/usr/bin/python3

from pydantic import BaseSettings


class MiddlewareMessage(BaseSettings):
    # 请求成功
    SUCCESS = 20000
    # 请求失败
    ERROR = 20001
    # 没有权限
    UNAUTHORIZED = 40001
    # 拒绝访问
    FORBIDDEN = 40003
    # 不存在
    NOT_FOUND = 40004
    # 服务器错误
    NETWORK = 50000
    # 禁止访问地址
    FORBIDDEN_MESSAGE = 'Forbidden Access URL'
    # 单次请求记录超过限制
    PAGE_SIZE_MESSAGE = 'Exceeded Single Page Request Record Limit'
    # 没有登录
    NOT_LOGIN_MESSAGE = 'Please Login System'
    # 令牌为空
    TOKEN_EMPTY_MESSAGE = 'Token Is Not Provided'
    # 令牌过期
    TOKEN_EXPIRED_MESSAGE = 'Token Is Expired'
    # 用户被禁用
    USER_DISABLED_MESSAGE = 'User Is Disabled'
    # 角色不存在
    ROLE_NOT_EXIST_MESSAGE = 'Role Is Not Exists'
    # 角色被禁用
    ROLE_DISABLED_MESSAGE = 'Role Is Disabled'
    # 用户不存在
    USER_NOT_FOUND_MESSAGE = 'User Not Found'
    # 不登录可以访问地址
    NOT_LOGIN_ACCESS_URL = ['/api/v1/account/login', '/api/v1/common/captcha', '/api/v1/account/register']


middlewareMessage = MiddlewareMessage()
