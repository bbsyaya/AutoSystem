# coding=utf-8
from __future__ import unicode_literals, absolute_import

import logging

__author__ = 'GoTop'

from .base import *

SETTING_FILE = 'production'

MEDIA_ROOT = '/home/gotop/Media/'

os.environ[
    'REQUESTS_CA_BUNDLE'] = '/home/gotop/.virtualenvs/AutoSystem/lib/python2' \
                            '.7/site-packages/certifi/cacert.pem'

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

# reference: http://www.marinamele.com/use-the-google-analytics-api-with-django
CLIENT_SECRETS = os.path.join(
    os.path.dirname(__file__), 'client_secret.json')
REDIRECT_URI = 'http://139.162.49.187.xip.io/oauth2/oauth2callback'
SCOPES = 'https://www.googleapis.com/auth/youtube'
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

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
# CELERY_ALWAYS_EAGER = True


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

# This allows you to easily change the schedules, even while Django and
# Celery are running.
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


class SuppressDeprecated(logging.Filter):
    def filter(self, record):
        WARNINGS_TO_SUPPRESS = [
            'RemovedInDjango18Warning',
            'RemovedInDjango19Warning'
        ]
        # Return false to suppress message.
        return not any(
            [warn in record.getMessage() for warn in WARNINGS_TO_SUPPRESS])


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'suppress_deprecated': {
            '()': 'AutoSystem.settings.SuppressDeprecated'
        }
    },

    'formatters': {
        'verbose': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s|%(message)s'
        },
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['suppress_deprecated']
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 0,
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'AutoSystem': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
        'myapp.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'video': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'myapp.management': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'video.models': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
