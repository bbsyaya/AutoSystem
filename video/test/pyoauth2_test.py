# coding=utf-8
from __future__ import unicode_literals
from AutoSystem import settings

__author__ = 'GoTop'

from pyoauth2 import Client

CLIENT_ID = client_id=settings.YOUKU_CLIENT_ID
CLIENT_SECRET = settings.YOUKU_CLIENT_SECRET
REDIRECT_URL = 'http://127.0.0.1:8000'
SCOPE = ''

youku_authorize_url='https://openapi.youku.com/v2/oauth2/authorize'
youku_token_url = 'https://openapi.youku.com/v2/oauth2/token'

#SCOPE = ['https://www.googleapis.com/auth/userinfo.profile',
#          'https://www.googleapis.com/auth/userinfo.email',]
#SCOPE = ' '.join(SCOPE)

client = Client(CLIENT_ID, CLIENT_SECRET,
                site='https://openapi.youku.com/v2',
                authorize_url=youku_authorize_url,
                token_url=youku_token_url)

print '-' * 80
authorize_url = client.auth_code.authorize_url(redirect_uri=REDIRECT_URL,
                                               scope=SCOPE)
print 'Go to the following link in your browser:'
print authorize_url

code = raw_input('Enter the verification code and hit ENTER when you\'re done:')
code = code.strip()
access_token = client.auth_code.get_token(code, redirect_uri=REDIRECT_URL)
print 'token', access_token.headers

print '-' * 80
print 'get user info'
ret = access_token.get('/users/myinfo.json')
print ret.parsed