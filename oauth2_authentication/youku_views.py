# coding=utf-8
from __future__ import unicode_literals
import json
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

__author__ = 'GoTop'

from django.contrib.auth.decorators import login_required
from AutoSystem import settings
from function.youku import youku_get_authenticate_online

from pyoauth2 import Client
import django_settings

CLIENT_ID = client_id = settings.YOUKU_CLIENT_ID
CLIENT_SECRET = settings.YOUKU_CLIENT_SECRET
REDIRECT_URL = 'http://127.0.0.1:8000/oauth2/youku_oauth2callback'
SCOPE = ''

YOUKU_AUTHORIZE_URL = 'https://openapi.youku.com/v2/oauth2/authorize'
YOUKU_TOKEN_URL = 'https://openapi.youku.com/v2/oauth2/token'


@login_required
def youku_authenticate_view(request):
    """
    通过django_settings，在数据库中查找之前获取到的access token

    :param request:
    :return:
    """
    # 在本地获取youku_access_token
    youku_access_token = django_settings.get('youku_access_token', default=None)

    if youku_access_token is None:
        # 到youtube获取access token
        youku_access_token = youku_get_authenticate_online(request)

    return youku_access_token


@login_required
def youku_oauth2callback_view(request):
    """
    将认证后的返回的授权码,用于获取access token
    :param request:
    :return:
    """
    code = request.GET.get('code')
    code = code.strip()
    client = Client(CLIENT_ID, CLIENT_SECRET,
                    site='https://openapi.youku.com/v2',
                    authorize_url=YOUKU_AUTHORIZE_URL,
                    token_url=YOUKU_TOKEN_URL)

    access_token = client.auth_code.get_token(code, redirect_uri=REDIRECT_URL)
    django_settings.set('String', 'youku_access_token', access_token)
    return render_to_response('result.html',
                              {'text': access_token.token})
