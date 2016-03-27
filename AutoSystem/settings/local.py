# coding=utf-8
from __future__ import unicode_literals, absolute_import

__author__ = 'GoTop'

from .base import *

SETTING_FILE = 'local'

MEDIA_ROOT = 'E:/media/'

# from AutoSystem.settings.flowerconfig import  *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True
INSTALLED_APPS += (
    # 'debug_toolbar', # and other apps for local development
)


YOUTUBE_DOWNLOAD_DIR = 'E:\Media\Video\YouTube\\'
FFMPEG_LOCATION = 'E:\\Program Files\\ffmpeg\\bin'

# 访问 https://openapi.youku.com/v2/oauth2/authorize?client_id=bdf4fcf59c05aff9
# &response_type=code&redirect_uri=http
# ://127.0.0.1:8000
# 可获得Authorization Code
# 再用post的方式，用Authorization Code去获取access token
YOUKU_CLIENT_ID = "bdf4fcf59c05aff9"
YOUKU_CLIENT_SECRET = "6acb15a83ec6eb8ebb5e7db6ccbaf283"
REDIRECT_URL = 'http://127.0.0.1:8000/oauth2/youku_oauth2callback'



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



DEBUG_TOOLBAR_PATCH_SETTINGS = False

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]
    SHOW_TOOLBAR_CALLBACK = True

    INTERNAL_IPS = ('127.0.0.1',)
