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
YOUKU_CLIENT_ID = "77e7308f29201c63"
YOUKU_CLIENT_SECRET = "0dbdd25be16ee0bc7aa6427b3d04148b"
REDIRECT_URL = 'http://139.162.49.187/oauth2/youku_oauth2callback'


ALLOWED_HOSTS = ['*']
