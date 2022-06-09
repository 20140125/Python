#!/usr/bin/python3
import json
import urllib.parse

import requests
from requests import JSONDecodeError

from vendor import get_state, helper

"""
OsChina API 授权登录
"""


class OsChina:

    def __init__(self, *, appid, app_secret, redirect_uri):
        self.appid = appid
        self.app_secret = app_secret
        self.redirect_uri = '{}{}'.format(helper.settings.app_host, redirect_uri)
        self.api_url = 'https://www.oschina.net/'

    async def get_auth_url(self, length):
        """
        todo:获取授权地址
        :param length:
        :return:
        """
        params = {
            'client_id': self.appid,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'state': await get_state(length),
        }
        return '{}action/oauth2/authorize?{}'.format(self.api_url, urllib.parse.urlencode(params))

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
                'client_secret': self.app_secret,
                'dataType': 'json',
                'callback': 'json'
            }
            result = requests.post('{}action/openapi/token'.format(self.api_url), data=json.dumps(params))
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
                'client_id': self.appid,
                'redirect_uri': self.redirect_uri,
                'client_secret': self.app_secret,
                'refresh_token': refresh_token,
                'dataType': 'json',
                'callback': 'json'
            }
            result = requests.post('{}action/openapi/token'.format(self.api_url), data=json.dumps(params))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'refresh_access_token failed'}

    async def get_user_info(self, access_token):
        """
        todo: 获取用户信息
        :param access_token:
        :return:
        """
        try:
            params = {
                'access_token': access_token,
                'dataType': 'json',
            }
            result = requests.post('{}action/openapi/user'.format(self.api_url), data=json.dumps(params))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_user_info failed'}


OsChinaAuth = OsChina(appid=helper.settings.os_china_appid, app_secret=helper.settings.os_china_app_secret, redirect_uri=helper.settings.os_china_redirect_uri)
