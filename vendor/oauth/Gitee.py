#!/usr/bin/python3
import json
import urllib.parse

import requests
from requests import JSONDecodeError

from vendor.oauth import get_state, helper

"""
Gitee API 授权登录
"""


class Gitee:

    def __init__(self, *, appid, app_secret, redirect_uri):
        self.appid = appid
        self.app_secret = app_secret
        self.redirect_uri = '{}{}'.format(helper.settings.app_host, redirect_uri)
        self.api_url = 'https://gitee.com/'

    async def get_auth_url(self, length, scope='user_info'):
        """
        todo:获取授权地址
        :param length:
        :param scope:
        :return:
        """
        params = {
            'client_id': self.appid,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': scope,
            'state': await get_state(length),
        }
        return '{}oauth/authorize?{}'.format(self.api_url, urllib.parse.urlencode(params))

    async def get_access_token(self, code):
        """
        todo: 获取access_token
        :param code:
        :return:
        """
        try:
            params = {
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': self.appid,
                'redirect_uri': self.redirect_uri,
                'client_secret': self.app_secret
            }
            result = requests.post('{}oauth/token'.format(self.api_url), data=json.dumps(params))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_access_token failed'}

    async def refresh_access_token(self, refresh_token):
        """
        todo:刷新access_token
        :param refresh_token:
        :return:
        """
        try:
            params = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }
            result = requests.post('{}oauth/token'.format(self.api_url), data=json.dumps(params))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'refresh_access_token failed'}

    async def get_user_info(self, access_token):
        """
        todo:获取用户信息
        :param access_token:
        :return:
        """
        try:
            params = {
                'access_token': access_token
            }
            result = requests.get('{}api/v5/user?{}'.format(self.api_url, urllib.parse.urlencode(params)))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_user_info failed'}


GiteeAuth = Gitee(appid=helper.settings.gitee_appid, app_secret=helper.settings.gitee_app_secret, redirect_uri=helper.settings.gitee_redirect_uri)
