# coding=utf-8
from __future__ import unicode_literals

__author__ = 'GoTop'

import os
import logging
import httplib2

from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django_sample.plus.models import CredentialsModel
from django_sample import settings
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/plus.me',
    redirect_uri='http://localhost:8000/oauth2callback')


@login_required
def index(request):
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    # 如果credential为空，或者无效，则将网页重定位到认证页面，让用户登陆认证
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("plus", "v1", http=http)
        activities = service.activities()
        activitylist = activities.list(collection='public',
                                       userId='me').execute()
        logging.info(activitylist)

        return render(request, 'plus/welcome.html', {
            'activitylist': activitylist,
        })


@login_required
def auth_return(request):
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'],
                                   request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.REQUEST)
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/")


drive_service = build('drive', 'v2', http=http_auth)

flow = client.flow_from_clientsecrets(
    'client_secrets.json',
    scope='https://www.googleapis.com/auth/youtube',
    redirect_uri='http://www.example.com/oauth2callback')

auth_uri = flow.step1_get_authorize_url()

credentials = flow.step2_exchange(auth_code)
http_auth = credentials.authorize(httplib2.Http())

drive_service = build('drive', 'v2', http=http_auth)

files = drive_service.files().list().execute()

flow = client.flow_from_clientsecrets(...)
flow.params['access_type'] = 'offline'