# coding=utf-8
from __future__ import unicode_literals
from adminbrowse import AutoBrowseModelAdmin, link_to_url, link_to_changelist, link_to_change
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import Video


# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_cn', 'thumbnail_image', 'publishedAt', 'show_youtube_url', 'show_youku_url', 'file')
    list_editable = ['title_cn']
    readonly_fields = ('publishedAt',)
    list_per_page = 10
    search_fields = ('title', 'title_cn')

    def show_youtube_url(self, obj):
        return format_html("<a href='{youtube_url}' target='_blank'>{youtube_url}</a>",
                           youtube_url='https://www.youtube.com/watch?v=%s' % obj.video_id)

    show_youtube_url.allow_tags = True

    def show_youku_url(self, obj):
        if obj.youku_id:
            return format_html("<a href='{youku_url}' target='_blank'>{youku_url}</a>",
                               youku_url='http://v.youku.com/v_show/id_%s.html' % obj.youku_id)
        else:
            return format_html("<a href='{publish_youku_url}' target='_blank'>{publish_youku_url}</a>",
                               publish_youku_url= reverse('video:youku_upload',args=[obj.video_id]))
    show_youku_url.allow_tags = True

    def download_youtube_url(self, obj):
        if obj.file:
            return obj.file
        else:
            return format_html("<a href='{download_youtube_url}' target='_blank'>{download_youtube_url}</a>",
                               download_youtube_url=reverse('video:download_youtube', args=[obj.video_id]))

    show_youku_url.allow_tags = True

admin.site.register(Video, VideoAdmin)
