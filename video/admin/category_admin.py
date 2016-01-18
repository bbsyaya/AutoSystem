# coding=utf-8
from __future__ import unicode_literals

__author__ = 'GoTop'

from django.contrib import admin
from video.models import Category


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
