# coding=utf-8
from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
import django_settings
from pyoauth2 import Client
from AutoSystem import settings

__author__ = 'GoTop'

CLIENT_ID = settings.YOUKU_CLIENT_ID
CLIENT_SECRET = settings.YOUKU_CLIENT_SECRET
REDIRECT_URL = 'http://127.0.0.1:8000/oauth2/youku_oauth2callback'
SCOPE = ''

YOUKU_AUTHORIZE_URL = 'https://openapi.youku.com/v2/oauth2/authorize'
YOUKU_TOKEN_URL = 'https://openapi.youku.com/v2/oauth2/token'


def youku_get_authenticate():
    """
    获取access_token
    :return:
    """
    # 在本地获取youku_access_token
    youku_access_token = django_settings.get('youku_access_token', default=None)
    if youku_access_token is None:
        # 到youku获取access token
        # 但是转到youku的认证页面之后再也无法转回来了
        return HttpResponseRedirect(reverse('oauth2_authentication:youku_authenticate'))
    else:
        return youku_access_token

