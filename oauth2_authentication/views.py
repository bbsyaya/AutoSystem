# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
import os
import httplib2
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

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


# reference: http://www.marinamele.com/use-the-google-analytics-api-with-django
CLIENT_SECRETS = os.path.join(
    os.path.dirname(__file__), 'client_secret.json')

REDIRECT_URI = 'http://127.0.0.1:8000/oauth2/oauth2callback'
SCOPES = 'https://www.googleapis.com/auth/youtube'


def get_account_ids(service):
    accounts = service.management().accounts().list().execute()
    ids = []
    if accounts.get('items'):
        for account in accounts['items']:
            ids.append(account['id'])
    return ids


def get_playlists_view(request):
    service = get_authenticated_service(request)
    playlists_request = service.liveBroadcasts().list(
        part="id,snippet",
        maxResults=50
    )

    while playlists_request:
        playlists_response = playlists_request.execute()

        for playlist in playlists_response.get("items", []):
            print "%s (%s)" % (playlist["snippet"]["title"], playlist["id"])

        list_broadcasts_request = service.liveBroadcasts().list_next(
            playlists_request, playlists_response)


def search_view(request, q, max_results):
    """
    在youtube上搜索关键字q，返回结果数设置为max_results

    :param request:
    :param q:
    :param max_results:
    :return:
    """
    service = get_authenticated_service(request)
    search_response = service.search().list(
        q=q,
        part="id,snippet",
        maxResults=max_results
    ).execute()

    videos = []

    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                       search_result["id"]["videoId"]))
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                         search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                          search_result["id"]["playlistId"]))


@login_required
def get_authenticated_service(request):
    """
    让用户到google上进行认证，返回认证后的http服务
    :param request:
    :return:
    """
    FLOW = flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    user = request.user
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    credential = storage.get()

    if credential is None or credential.invalid is True:
        # there will be some error show I ignore the validate part
        # FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, user)
        authorize_url = FLOW.step1_get_authorize_url()
        f = FlowModel(id=user, flow=FLOW)
        f.save()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build('youtube', 'v3', http=http)
        return service


@login_required
def oauth2callback_view(request):
    """
    在google上确认授权之后，会转到这个页面
    :param request:
    :return:
    """
    user = request.user
    # there will be some error show I ignore the validate part
    # if not xsrfutil.validate_token(
    # settings.SECRET_KEY, request.REQUEST['state'], user):
    # return HttpResponseBadRequest()

    # I have to use socks5 proxy to access google, because I live in China
    # http = httplib2.Http(proxy_info=httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 8115))

    FLOW = FlowModel.objects.get(id=user).flow
    credential = FLOW.step2_exchange(request.REQUEST)
    # 保存认证
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/oauth2")


@login_required
def index(request):
    service = get_authenticated_service(request)