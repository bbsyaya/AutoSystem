# coding=utf-8
from __future__ import unicode_literals
import json
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

__author__ = 'GoTop'

from django.contrib.auth.decorators import login_required
from AutoSystem import settings


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
    先通过django_settings，在数据库中查找之前获取到的access token
    如果本地没有，就到优酷上去获取,会跳转到youku的认证页面
    :param request:
    :return:
    """
    client = Client(CLIENT_ID, CLIENT_SECRET,
                    site='https://openapi.youku.com/v2',
                    authorize_url=YOUKU_AUTHORIZE_URL,
                    token_url=YOUKU_TOKEN_URL)

    authorize_url = client.auth_code.authorize_url(redirect_uri=REDIRECT_URL,
                                                   scope=SCOPE)
    return HttpResponseRedirect(authorize_url)


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

    #由youku认证页面转来的，没有request.META.HTTP_REFERER变量
    # 所以无法设置其返回前面的页面
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render_to_response('result.html',{'text': access_token.token})
