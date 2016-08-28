# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response

# Create your views here.
import os
import httplib2
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets, Storage
#from oauth2client.django_orm import Storage

from googleapiclient.discovery import build

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.contrib.sites.models import get_current_site

from oauth2_authentication.models import CredentialsModel, FlowModel
from AutoSystem.settings import CLIENT_SECRETS, SCOPES, REDIRECT_URI, \
    YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, SETTING_FILE


# reference: http://www.marinamele.com/use-the-google-analytics-api-with-django
@login_required
def authenticate_view(request):
    """
    进行google账号认证
    https://developers.google.com/identity/protocols/OAuth2WebServer
    :param request:
    :return:

    """
    result = get_authenticated_service(request.user)

    if result is None:
        # 如果未在本地查找到认证文件，则重定向到指定的authorize_url
        flow = flow_from_clientsecrets(
            CLIENT_SECRETS,
            scope=SCOPES,
            redirect_uri=REDIRECT_URI
        )

        flow.params['access_type'] = 'offline'

        # there will be some error show I ignore the validate part
        # FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
        #  user)

        # Generate a URL to request access from Google's OAuth 2.0 server
        authorize_url = flow.step1_get_authorize_url()
        user = request.user
        f = FlowModel(id=user, flow=flow)
        f.save()
        # 根据urls.py的设置，会调用oauth2callback_view()，打开authorize_url进行认证
        return HttpResponseRedirect(authorize_url)

    else:
        # 如果返回的是认证后的service，则显示成功获取的文字即可
        return render_to_response('result.html',
                                  {'text': '本地保存有认证文件'})


def get_authenticated_service(user):
    """
    让用户到google上进行认证，返回认证后的http服务
    :param request:
    :return:
    """
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    credential = storage.get()

    if credential is None or credential.invalid is True:
        result = None
    else:
        SETTING_FILE = 'production'
        # 如果是VPS中运行，则不使用代理
        if SETTING_FILE == 'production':
            http = httplib2.Http()
            http = credential.authorize(http)

        # 如果是本地运行，则使用代理
        if SETTING_FILE == 'local':
            myproxy = httplib2.ProxyInfo(
                proxy_type=httplib2.socks.PROXY_TYPE_SOCKS5,
                proxy_host='127.0.0.1', proxy_port=8115)
            http = httplib2.Http(proxy_info=myproxy)
            http = credential.authorize(http)

        service = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        http=http)
        result = service
    return result


@login_required
def oauth2callback_view(request):
    """
    在google上确认授权之后，会转到这个页面,保存获取到的认证码
    :param request:
    :return:
    """
    user = request.user
    # there will be some error show I ignore the validate part
    # if not xsrfutil.validate_token(
    # settings.SECRET_KEY, request.REQUEST['state'], user):
    # return HttpResponseBadRequest()

    # I have to use socks5 proxy to access google, because I live in China
    # http = httplib2.Http(proxy_info=httplib2.ProxyInfo(
    # httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 8115))
    flow = FlowModel.objects.get(id=user).flow
    # To exchange an authorization code for an access token
    credential = flow.step2_exchange(request.REQUEST)
    # 保存认证
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/oauth2")


@login_required
def reauthorize_view(request):
    user = request.user
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    if storage:
        storage.delete()
        text = '删除本地认证文件！'

    else:
        text = '在本地没有对应的storage文件，未能删除本地认证文件'

    return render_to_response('result.html',
                              {'text': text}
                              )
