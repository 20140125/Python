#!/usr/bin/python3
import urllib.parse

import requests
from requests import JSONDecodeError

from vendor import get_state, helper

"""
Baidu API 授权登录
"""


class Baidu:

    def __init__(self, *, appid, app_secret, redirect_uri):
        self.appid = appid
        self.app_secret = app_secret
        self.redirect_uri = '{}{}'.format(helper.settings.app_host, redirect_uri)
        self.api_url = 'https://openapi.baidu.com/'

    async def get_auth_url(self, length, scope='basic super_msg'):
        """
        todo:获取授权地址
        :param length
        :param scope
        display:
            desc
            page：全屏形式的授权页面(默认)，适用于web应用。
            popup: 弹框形式的授权页面，适用于桌面软件应用和web应用。
            dialog: 浮层形式的授权页面，只能用于站内web应用。
            mobile: IPhone / Android等智能移动终端上用的授权页面，适用于IPhone / Android等智能移动终端上的应用。
            pad: IPad / Android等平板上使用的授权页面，适用于IPad / Android等智能移动终端上的应用。
            tv: 电视等超大显示屏使用的授权页面。
        """
        params = {
            'response_type': 'code',
            'client_id': self.appid,
            'redirect_uri': self.redirect_uri,
            'scope': scope,
            'state': await get_state(length),
            'display': 'dialog',
            'force_login': '0',  # 如传递 'force_login=1'，则加载登录页时强制用户输入用户名和口令，不会从cookie中读取百度用户的登陆状态
            'confirm_login': '1',  # 如传递 'confirm_login=1' 且百度用户已处于登陆状态，会提示是否使用已当前登陆用户对应用授权。
            'login_type': 'sms'  # 如传递 'login_type=sms'，授权页面会默认使用短信动态密码注册登陆方式。
        }
        return '{}oauth/2.0/authorize?'.format(self.api_url, urllib.parse.urlencode(params))

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
            result = requests.get('{}oauth/2.0/token?'.format(self.api_url, urllib.parse.urlencode(params)))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_access_token failed'}

    async def refresh_access_token(self, refresh_token, scope='basic'):
        """
        todo: 获取access_token
        :param refresh_token:
        :param scope:
        :return:
        """
        try:
            params = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': self.appid,
                'client_secret': self.app_secret,
                'scope': scope
            }
            result = requests.get('{}oauth/2.0/token?{}'.format(self.api_url, urllib.parse.urlencode(params)))
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
                'format': 'json',
                'get_unionid': 1
            }
            result = requests.get('{}rest/2.0/passport/users/getInfo?{}'.format(self.api_url, urllib.parse.urlencode(params)))
            return result.json()
        except JSONDecodeError:
            return {'code': helper.code.ERROR, 'message': 'get_user_info failed'}


BaiduAuth = Baidu(appid=helper.settings.baidu_appid, app_secret=helper.settings.baidu_app_secret, redirect_uri=helper.settings.baidu_redirect_uri)
