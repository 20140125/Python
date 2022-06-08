#!/usr/bin/python3
import urllib.parse

import requests
from requests import JSONDecodeError

from vendor import get_state, helper

"""
QQ API 授权登录
"""


class QQ:

    # 构造函数
    def __init__(self, *, appid, app_secret, redirect_uri):
        self.appid = appid
        self.app_secret = app_secret
        self.redirect_uri = '{}{}'.format(helper.settings.app_host, redirect_uri)
        self.api_url = 'https://graph.qq.com/'

    async def get_auth_url(self, length=32, scope='get_user_info'):
        """
        todo:获取授权地址
        :param length:
        :param scope:
        :return:
        """
        params = {
            'response_type': 'code',
            'client_id': self.appid,
            'redirect_uri': self.redirect_uri,
            'state': await get_state(length),
            'scope': scope,
            'display': ''
        }
        return '{}oauth2.0/authorize?{}'.format(self.api_url, urllib.parse.urlencode(params))

    async def get_access_token(self, code):
        """
        todo:获取access_token
        :param code:
        :return:
        """
        try:
            params = {
                'grant_type': 'authorization_code',
                'client_id': self.appid,
                'client_secret': self.app_secret,
                'code': code,
                'redirect_uri': self.redirect_uri,
                'fmt': 'json'
            }
            result = requests.get('{}oauth2.0/token?{}'.format(self.api_url, urllib.parse.urlencode(params)))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_access_token failed'}

    async def refresh_access_token(self, refresh_token):
        """
        todo：刷新access_token
        :param refresh_token:
        :return:
        """
        try:
            params = {
                'grant_type': 'refresh_token',
                'client_id': self.appid,
                'client_secret': self.app_secret,
                'refresh_token': refresh_token,
                'fmt': 'json'
            }
            result = requests.get('{}oauth2.0/token?{}'.format(self.api_url, urllib.parse.urlencode(params)))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_access_token failed'}

    async def get_openid(self, access_token):
        """
        todo: 获取openid
        :param access_token:
        :return:
        """
        try:
            params = {
                'access_token': access_token,
                'fmt': 'json'
            }
            result = requests.get('{}oauth2.0/me?{}'.format(self.api_url, urllib.parse.urlencode(params)))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_openid failed'}

    async def get_user_info(self, access_token):
        """
        todo:获取用户信息
        :param access_token:
        :return:
        """
        param = await self.get_openid(access_token)
        try:
            params = {
                'access_token': access_token,
                'oauth_consumer_key': param['client_id'],
                'openid': param['openid'],
                'fmt': 'json'
            }
            result = requests.get('{}user/get_user_info?{}'.format(self.api_url, urllib.parse.urlencode(params)))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_user_info failed'}


QQAuth = QQ(appid=helper.settings.qq_appid, app_secret=helper.settings.qq_app_secret, redirect_uri=helper.settings.qq_redirect_uri)
