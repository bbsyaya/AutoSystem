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


# 使用django自带broker的设置
# 需要自己用命令python manage.py shell启动shell，在里面测试，不能直接用PyCharm的console
# BROKER_URL = 'django://'
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Europe/Madrid'

# CELERY SETTINGS
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'redis'
CELERY_TIMEZONE = 'Asia/Shanghai'

# That is, tasks will be executed locally instead of being sent to the queue.
# 用于测试环境，可以不开启worker，和broker
#CELERY_ALWAYS_EAGER = True


# 使用redis的设置
# BROKER_HOST = "localhost"
# BROKER_BACKEND="redis"
# REDIS_PORT=6379
# REDIS_HOST = "localhost"
# BROKER_USER = ""
# BROKER_PASSWORD =""
# BROKER_VHOST = "0"
# REDIS_DB = 0
# REDIS_CONNECT_RETRY = True
# CELERY_SEND_EVENTS=True
# CELERY_RESULT_BACKEND='redis'
# CELERY_TASK_RESULT_EXPIRES =  10
# CELERYBEAT_SCHEDULER="djcelery.schedulers.DatabaseScheduler"

import djcelery
djcelery.setup_loader()