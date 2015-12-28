# coding=utf-8
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from oauthlib.oauth2 import Client

__author__ = 'GoTop'

CLIENT_ID = client_id = settings.YOUKU_CLIENT_ID
CLIENT_SECRET = settings.YOUKU_CLIENT_SECRET
REDIRECT_URL = 'http://127.0.0.1:8000/oauth2/youku_oauth2callback'
SCOPE = ''

YOUKU_AUTHORIZE_URL = 'https://openapi.youku.com/v2/oauth2/authorize'
YOUKU_TOKEN_URL = 'https://openapi.youku.com/v2/oauth2/token'

def youku_get_authenticate_online(request):
    """
    让用户到youku上进行认证，返回认证后的http服务
    :param request:
    :return:
    """
    client = Client(CLIENT_ID, CLIENT_SECRET,
                    site='https://openapi.youku.com/v2',
                    authorize_url=YOUKU_AUTHORIZE_URL,
                    token_url=YOUKU_TOKEN_URL)

    print '-' * 80
    authorize_url = client.auth_code.authorize_url(redirect_uri=REDIRECT_URL,
                                                   scope=SCOPE)
    return HttpResponseRedirect(authorize_url)