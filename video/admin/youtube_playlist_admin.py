# coding=utf-8
from __future__ import unicode_literals
from django.core.urlresolvers import reverse

__author__ = 'GoTop'

from django.contrib import admin
from video.models import YouTubePlaylist


class YouTubePlaylistAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'show_playlist_url', 'show_thumbnail',
        'video_num', 'description','is_download',
        'show_change_channel_url',
        'show_video_of_playlist',
        'get_playlist_video_info_url', 'remark')
    list_per_page = 50
    search_fields = ('title',)
    list_filter = ('is_download','channel',)

    # 设置在change和edit页面显示哪些field
    # fieldsets = (
    #     ('None', {'fields': '__all__'}),
    # )

    # 一定要在后面加入逗号
    list_select_related = (
        'channel',
    )

    def show_playlist_url(self, obj):
        playlist_url = 'https://www.youtube.com/playlist?list=' + \
                       obj.playlist_id
        return "<a href='%s' target='_blank'>播单Url</a>" % playlist_url

    show_playlist_url.allow_tags = True
    show_playlist_url.short_description = 'Url'

    def show_thumbnail(self, obj):
        return '<img src="%s" width="50" height="50"/>' % obj.thumbnail

    show_thumbnail.allow_tags = True
    show_thumbnail.short_description = 'Thumbnail'

    def show_change_channel_url(self, obj):
        url = reverse("admin:video_youtubechannel_change",
                      args=[obj.channel.channel_id])
        return "<a href='%s' target='_blank'>%s</a>" % (url, obj.channel.title)

    show_change_channel_url.allow_tags = True
    show_change_channel_url.short_description = '查看channel'

    def show_video_of_playlist(self, obj):
        change_url = reverse('admin:video_video_changelist')
        extra = "?playlist__title__exact=%s" % (obj.title)
        return "<a href='%s' target='_blank'>播单视频</a>" % \
               (change_url + extra)

    show_video_of_playlist.allow_tags = True
    show_video_of_playlist.short_description = '播单视频'

    def get_playlist_video_info_url(self, obj):
        get_playlist_video_url = reverse(
            'video:get_youtube_playlist_video_info',
            args=[obj.playlist_id, 50])
        return "<a href='%s' target='_blank'>获取播单视频信息</a>" % \
               get_playlist_video_url

    get_playlist_video_info_url.allow_tags = True
    get_playlist_video_info_url.short_description = '获取播单视频信息'


admin.site.register(YouTubePlaylist, YouTubePlaylistAdmin)
