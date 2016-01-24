# coding=utf-8
from __future__ import unicode_literals

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from video.forms import ButtonWidget, YoukuForm

__author__ = 'GoTop'

from django.contrib import admin
from django import forms
from video.models import Youku


class YoukuAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags', 'published',)
    readonly_fields = ('published',)
    form = YoukuForm
    pass


admin.site.register(Youku, YoukuAdmin)
