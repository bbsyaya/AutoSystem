# coding=utf-8
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

__author__ = 'GoTop'

"""
使用django作为celery的broker时，在admin页面查看Queue
"""

from kombu.transport.django import models as kombu_models
admin.site.register(kombu_models.Message)
