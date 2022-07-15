#!/usr/bin/python3
import json
import urllib.parse

import requests
from requests import JSONDecodeError

from vendor.oauth import get_state, helper

"""
Github API 授权登录
"""


class Github:

    def __init__(self, *, appid, app_secret, redirect_uri):
        self.appid = appid
        self.app_secret = app_secret
        self.redirect_uri = '{}{}'.format(helper.settings.app_host, redirect_uri)
        self.api_url = 'https://github.com/'

    async def get_auth_url(self, length=32, scope='user:email'):
        """
        todo: 获取授权登录地址
        :param length:
        :param scope:
        :return:
        """
        params = {
            'client_id': self.appid,
            'redirect_uri': self.redirect_uri,
            'scope': scope,
            'state': await get_state(length),
            'allow_signup': True  # 是否在登录页显示注册，默认false
        }
        return '{}login/oauth/authorize?{}'.format(self.api_url, urllib.parse.urlencode(params))

    async def get_access_token(self, code, state):
        """
        todo: 获取access_token
        :param code:
        :param state:
        :return:
        """
        try:
            params = {
                'client_id': self.appid,
                'client_secret': self.app_secret,
                'code': code,
                'redirect_uri': self.redirect_uri,
                'state': state
            }
            result = requests.post('{}login/oauth/access_token'.format(self.api_url), data=json.dumps(params))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_access_token failed'}

    @staticmethod
    async def get_user_info(access_token):
        """
        todo 获取用户信息
        :param access_token:
        :return:
        """
        try:
            headers = {
                'Authorization': 'token {}'.format(access_token),
            }
            result = requests.get('https://api.github.com/user', headers=headers)
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_user_info failed'}

    @staticmethod
    async def get_user_repos(access_token):
        """
        todo: 获取access_token
        :param access_token:
        :return:
        """
        try:
            headers = {
                'Authorization': 'token {}'.format(access_token),
            }
            result = requests.get('https://api.github.com/user/repos', headers=headers)
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_user_repos failed'}


GithubAuth = Github(appid=helper.settings.github_appid, app_secret=helper.settings.github_app_secret, redirect_uri=helper.settings.github_redirect_uri)
