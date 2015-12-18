# coding=utf-8
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


#参考 http://www.marinamele.com/use-the-google-analytics-api-with-django
CLIENT_SECRETS = os.path.join(
    os.path.dirname(__file__), 'client_secret.json')


def get_account_ids(service):
    accounts = service.management().accounts().list().execute()
    ids = []
    if accounts.get('items'):
        for account in accounts['items']:
            ids.append(account['id'])
    return ids


@login_required
def index(request):
    # use the first REDIRECT_URI if you are developing your app
    # locally, and the second in production

    REDIRECT_URI = 'http://127.0.0.1:8000/oauth2/oauth2callback'
    # REDIRECT_URI = "%s%s" % (get_current_site(request).domain, reverse("oauth2:return"))
    FLOW = flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/analytics.readonly',
        redirect_uri=REDIRECT_URI
    )
    user = request.user
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid is True:
        FLOW.params['state'] = xsrfutil.generate_token(
            settings.SECRET_KEY, user)
        authorize_url = FLOW.step1_get_authorize_url()
        f = FlowModel(id=user, flow=FLOW)
        f.save()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build('analytics', 'v3', http=http)
        ids = get_account_ids(service)
        return render(
            request, 'oauth2_authentication/main.html', {'ids': ids})


@login_required
def auth_return(request):
    user = request.user
    if not xsrfutil.validate_token(
            settings.SECRET_KEY, request.REQUEST['state'], user):
        return HttpResponseBadRequest()
    FLOW = FlowModel.objects.get(id=user).flow
    credential = FLOW.step2_exchange(request.REQUEST)
    storage = Storage(CredentialsModel, 'id', user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/oauth2")
