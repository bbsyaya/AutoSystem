# coding=utf-8
from __future__ import unicode_literals, absolute_import

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

__author__ = 'GoTop'

from AutoSystem.settings import SCOPES, YOUTUBE_API_SERVICE_NAME, \
    YOUTUBE_API_VERSION, GOOGLE_KEY_FILE, SETTING_FILE


def get_authenticated_service_s2s():
    """
    使用oauth2 server to server的方式获取认证的google服务
    :param user:
    :return:
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_KEY_FILE,
        SCOPES)

    #SETTING_FILE = 'production'
    # 如果是VPS中运行，则不使用代理
    if SETTING_FILE == 'production':
        proxy_http = None

    # 如果是本地运行，则使用代理
    if SETTING_FILE == 'local':
        myproxy = httplib2.ProxyInfo(
            proxy_type=httplib2.socks.PROXY_TYPE_HTTP,
            proxy_host='127.0.0.1', proxy_port=8118)
        proxy_http = httplib2.Http(proxy_info=myproxy)

    youtube_service = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                            credentials=credentials, http=proxy_http)

    return youtube_service
