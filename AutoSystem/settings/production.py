# coding=utf-8
from __future__ import unicode_literals, absolute_import

__author__ = 'GoTop'

from .base import *

MEDIA_ROOT = '/home/gotop/Media/'

DEBUG = False
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