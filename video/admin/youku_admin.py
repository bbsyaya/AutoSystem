# coding=utf-8
from __future__ import unicode_literals

from video.forms import YoukuForm

__author__ = 'GoTop'

from django.contrib import admin
from video.models import Youku


class YoukuAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags', 'published',)
    readonly_fields = ('published',)
    form = YoukuForm

    def save_model(self, request, obj, form, change):
        # 如果form.changed_data中包含'youku_playlist'，说明更改了youku_playlist，
        # 要在旧的优酷playlist中删除youku_video_id视频，否则视频会属于多个playlist
        if 'youku_playlist' in form.changed_data:
            # todo 以下这段引用如果放在顶部则无法启动django server，原因未明
            from video.function.youku import delete_video_from_playlist, set_youku_playlist
            # 只要改变了field['youku_playlist']，自动在playlist_id的优酷playlist中删除youku_video_id视频
            old_youku_playlist_id = form.initial['youku_playlist']
            delete_video_from_playlist(obj.youku_video_id, old_youku_playlist_id)
            set_youku_playlist(obj.youku_video_id, form.cleaned_data['youku_playlist'].id)
        obj.save()


admin.site.register(Youku, YoukuAdmin)
