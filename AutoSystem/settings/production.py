# coding=utf-8
from __future__ import unicode_literals, absolute_import

__author__ = 'GoTop'

from .base import *

SETTING_FILE = 'production'

MEDIA_ROOT = '/home/gotop/Media/'

DEBUG = True
INSTALLED_APPS += (
    # other apps for production site
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'autosystem',
        'USER': 'autosystemuser',
        'PASSWORD': 'The19840520',
        'HOST': 'localhost',
        'PORT': '',
    }
}


YOUTUBE_DOWNLOAD_DIR = '/home/gotop/Media/Video/YouTube/'

FFMPEG_LOCATION = "/usr/bin/ffmpeg"
# 访问 https://openapi.youku.com/v2/oauth2/authorize?client_id=bdf4fcf59c05aff9
# &response_type=code&redirect_uri=http
# ://127.0.0.1:8000
# 可获得Authorization Code
# 再用post的方式，用Authorization Code去获取access token
YOUKU_CLIENT_ID = "a6aeb5ff9627346b"
YOUKU_CLIENT_SECRET = "1c2c6330b65fdb2a4cd3e20dee8fac22"


ALLOWED_HOSTS = ['*']
