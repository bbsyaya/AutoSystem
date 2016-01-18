# coding=utf-8
from __future__ import unicode_literals

__author__ = 'GoTop'

from django.contrib import admin
from video.models import BaiduYun


class BaiduYunAdmin(admin.ModelAdmin):
    pass


admin.site.register(BaiduYun, BaiduYunAdmin)
