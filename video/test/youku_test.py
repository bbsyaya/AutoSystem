# coding=utf-8
from __future__ import unicode_literals
from AutoSystem import settings

__author__ = 'GoTop'

from youku import YoukuUpload, YoukuOauth


def main():
    youku_oauth = YoukuOauth(settings.YOUKU_CLIENT_ID, settings.YOUKU_CLIENT_SECRET, redirect_uri='http://127.0.0.1:8000')

    ACCESS_TOKEN = youku_oauth.get_token_by_code(settings.YOUKU_AUTHORIZE_CODE)
    print(ACCESS_TOKEN)

main()