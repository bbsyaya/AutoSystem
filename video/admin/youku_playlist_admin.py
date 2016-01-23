# coding=utf-8
from __future__ import unicode_literals

__author__ = 'GoTop'

from django.contrib import admin
from video.models import YoukuPlaylist


class YoukuPlaylistAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'view_count','video_count','duration',)
    readonly_fields = ('view_count','video_count','duration',)
    pass

admin.site.register(YoukuPlaylist, YoukuPlaylistAdmin)
