# coding=utf-8
from __future__ import unicode_literals

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from video.forms import ButtonWidget

__author__ = 'GoTop'

from django.contrib import admin
from django import forms
from video.models import Youku


class YoukuForm(forms.ModelForm):
    button = forms.CharField(widget=ButtonWidget)

    class Meta:
        model = Youku

        # 覆盖默认的widget
        # https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#overriding-the-default-fields
        widgets = {
            'title': forms.TextInput(attrs={'size': 100}),
            'tags': forms.TextInput(attrs={'size': 100}),
        }
        fields = '__all__'  # Register your models here.


class YoukuAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags', 'published',)
    form = YoukuForm
    pass


admin.site.register(Youku, YoukuAdmin)
