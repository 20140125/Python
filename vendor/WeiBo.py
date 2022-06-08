#!/usr/bin/python3
import json
import urllib.parse

import requests
from requests import JSONDecodeError

from vendor import get_state, helper

"""
Gitee API 授权登录
"""


class WeiBo:

    def __init__(self, *, appid, app_secret, redirect_uri):
        self.appid = appid
        self.app_secret = app_secret
        self.redirect_uri = '{}{}'.format(helper.settings.app_host, redirect_uri)
        self.api_url = 'https://api.weibo.com/'

    async def get_auth_url(self, length, scope='all,email'):
        """
        todo:获取授权地址
        :param length:
        :param scope:
        :return:
        """
        params = {
            'client_id': self.appid,
            'display': 'default',  # default mobile wap client
            'forcelogin': False,  # 是否强制用户重新登录，true：是，false：否。默认false。
            'language': '',  # 授权页语言，缺省为中文简体版，en为英文版
            'redirect_uri': self.redirect_uri,
            'state': await get_state(length),
            'scope': scope
        }
        return '{}oauth/authorize?{}'.format(self.api_url, urllib.parse.urlencode(params))

    async def get_access_token(self, code):
        """
        todo:获取access_token
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
            result = requests.post('{}oauth2/access_token'.format(self.api_url), data=json.dumps(params))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_access_token failed'}

    async def get_user_info(self, access_token, uid):
        """
        todo:获取用户信息
        :param access_token:
        :param uid:
        :return:
        """
        try:
            params = {
                'access_token': access_token,
                'uid': uid
            }
            result = requests.get('{}2/users/show.json?{}'.format(self.api_url, urllib.parse.urlencode(params)))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_user_info failed'}


WeiBoAuth = WeiBo(appid=helper.settings.weibo_appid, app_secret=helper.settings.weibo_app_secret,
                  redirect_uri=helper.settings.weibo_redirect_uri)
