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

    # save_model()是保存该ModelAdmin,也就是在Youku的admin change和add页面保存youku对象时使用
    # 但是当在video的change页面的保存youku inline对象时，不使用该函数，
    # 使用的是videoadmin中的save_formset()函数
    # def save_model(self, request, obj, form, change):
    #     # 如果form.changed_data中包含'setted_youku_playlist'，说明更改了youku_playlist，
    #     # 要在旧的优酷playlist中删除youku_video_id视频，否则视频会属于多个playlist
    #     if 'setted_youku_playlist' in form.changed_data:
    #         # 如果设置的setted_youku_playlist与youku_playlist不相同，则要在优酷网上将video
    #         # 从youku_playlist中删除，然后再将video添加到setted_youku_playlist中，
    #         # 最后将本地数据库中的youku_playlist设置为setted_youku_playlist
    #         if form.initial['setted_youku_playlist'] <> form.initial[
    #             'youku_playlist']:
    #             # todo 以下这段引用如果放在顶部则无法启动django server，原因未明
    #             from video.function.youku import delete_video_from_playlist, \
    #                 set_youku_playlist_online
    #             # 只要改变了field['youku_playlist']，自动在playlist_id的优酷playlist
    #             # 中删除youku_video_id视频
    #             old_youku_playlist_id = form.initial['youku_playlist']
    #             delete_video_from_playlist(obj.youku_video_id,
    #                                        old_youku_playlist_id)
    #             playlist_id = set_youku_playlist_online(
    #                 obj.youku_video_id,
    #                 form.cleaned_data['setted_youku_playlist'].id)
    #             if playlist_id:
    #                 obj.youku_playlist = obj.setted_youku_playlist
    #
    #     obj.save()


admin.site.register(Youku, YoukuAdmin)
