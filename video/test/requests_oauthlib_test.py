# coding=utf-8
from __future__ import unicode_literals
from datetime import time
from requests import session
from AutoSystem import settings

import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

__author__ = 'GoTop'

from requests_oauthlib import OAuth2Session

client_id = settings.YOUKU_CLIENT_ID
client_secret = settings.YOUKU_CLIENT_SECRET
redirect_uri = 'http://127.0.0.1:8000'


def automatic_refresh():
    """Refreshing an OAuth 2 token using a refresh token.
    """
    token = session['oauth_token']

    # We force an expiration by setting expired at in the past.
    # This will trigger an automatic refresh next time we interact with
    # Googles API.
    token['expires_at'] = time() - 10

    extra = {
        'client_id': client_id,
        'client_secret': client_secret,
    }

    def token_updater(token):
        session['oauth_token'] = token

    google = OAuth2Session(client_id,
                           token=token,
                           auto_refresh_kwargs=extra,
                           auto_refresh_url=refresh_url,
                           token_updater=token_updater)

    # Trigger the automatic refresh
    jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())
    return jsonify(session['oauth_token'])


oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
authorization_url, state = oauth.authorization_url('https://openapi.youku.com/v2/oauth2/authorize')

print 'Please go to %s and authorize access.' % authorization_url
authorization_response = raw_input('Enter the full callback URL:')

token = oauth.fetch_token(
    'https://openapi.youku.com/v2/oauth2/token',
    authorization_response=authorization_response,
    client_secret=client_secret
)

r = oauth.post('https://openapi.youku.com/v2/users/myinfo.json',{'client_id' : client_id})
print r.content