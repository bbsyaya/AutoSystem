# coding=utf-8
from __future__ import unicode_literals
from AutoSystem import settings

__author__ = 'GoTop'

import oauth2 as oauth, urllib


def oauth_req(url, key, secret, http_method="POST", post_body=None, http_headers=None):
    CONSUMER_KEY = settings.YOUKU_CLIENT_ID
    CONSUMER_SECRET = settings.YOUKU_CLIENT_SECRET
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)
    resp, content = client.request(
        url,
        method=http_method,
        body=urllib.urlencode({'status': post_body}),
        headers=http_headers,
        force_auth_header=True,
    )
    return content

oauth_req('http://api.twitter.com/1/statuses/update.json', KEY, SECRET, post_body=MESSAGE)