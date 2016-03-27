# coding=utf-8
from __future__ import unicode_literals, absolute_import

__author__ = 'GoTop'

# coding=utf-8
"""
Django settings for AutoSystem project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.realpath(os.path.dirname(__file__) + "/.."))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm8auh#=gh!g9t2c=d8&*5(c&9oj6)2aubmkr#bik(%kgu70k%n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    # 'tinymce',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
    'django.contrib.sites',
    'django_settings',  # https://github.com/jqb/django-settings

    # 'kombu.transport.django',# Django-based broker, for use mainly during
    # development.
    'djcelery',
    'django_cleanup',
    # automatically deletes files for FileField, ImageField, and subclasses.
    # It will delete old files when a new file is being save and it will
    # delete files on model instance deletion.
    # 'manage_rss',
    # 'adminbrowse',

    # 'django_youtube',
    'oauth2_authentication',
    'video',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'AutoSystem.urls'

WSGI_APPLICATION = 'AutoSystem.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# add 2014-9-14
# django.contrib.staticfiles 要求设置STATIC_ROOT和MEDIA_ROOT，这样能自动收集所有的静态文件到指定的目录下
STATIC_ROOT = BASE_DIR + '/static/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    'manage_rss/static',
)

SITE_ID = 1

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

# http://stackoverflow.com/questions/20873625/pycharm-code-inspection
# -complains-template-file-not-found-how-to-fix
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

ADMINBROWSE_MEDIA_URL = STATIC_ROOT + '/adminbrowse/media/'

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    # 'skin': "o2k7",
    'theme_advanced_toolbar_location': "top",

    # Buttons/controls
    # http://www.tinymce.com/wiki.php/TinyMCE3x:Buttons/controls
    'theme_advanced_buttons1': "bold,italic,underline,separator,bullist,"
                               "separator,outdent,indent,separator,undo,redo",
    'theme_advanced_buttons2': "fontsizeselect,formatselect",
    'theme_advanced_buttons3': "",

    'theme_advanced_resizing': "true",
    'theme_advanced_font_sizes': "16px,24px",
    'font_size_style_values': "16px,18px,20px",
    'height': "600",
    'width': "800",
    'content_css': "/static/tinymce/content_css.css"
}

YOUTUBE_AUTH_EMAIL = 'imgotop@gmail.com'
YOUTUBE_AUTH_PASSWORD = ''
YOUTUBE_DEVELOPER_KEY = 'AIzaSyAp4Dr7YgwofjNbosQ5VZFXm8G5A1QNIPQ'
YOUTUBE_CLIENT_ID = '505556718060-20u5pd4rd7sgeigqmdc5o5rvt1ifjtfk.apps' \
                    '.googleusercontent.com'




YOUKU_AUTHORIZE_CODE = "6ba16e4808c2fd5767012465b497510f"
# https://openapi.youku.com/v2/oauth2/authorize?client_id=bdf4fcf59c05aff9
# &response_type=code




# http://stackoverflow.com/a/31103483/1314124
# 让django1.8.9不显示RemovedInDjango19Warning
import logging, copy
from django.utils.log import DEFAULT_LOGGING

LOGGING = copy.deepcopy(DEFAULT_LOGGING)
LOGGING['filters']['suppress_deprecated'] = {
    '()': 'AutoSystem.settings.SuppressDeprecated'
}
LOGGING['handlers']['console']['filters'].append('suppress_deprecated')


class SuppressDeprecated(logging.Filter):
    def filter(self, record):
        WARNINGS_TO_SUPPRESS = [
            'RemovedInDjango18Warning',
            'RemovedInDjango19Warning'
        ]
        # Return false to suppress message.
        return not any(
                [warn in record.getMessage() for warn in WARNINGS_TO_SUPPRESS])
