# coding=utf-8
from __future__ import unicode_literals
from adminbrowse import AutoBrowseModelAdmin, link_to_url, link_to_changelist, link_to_change
from django.utils.html import format_html

from django.contrib import admin
from .models import Video

# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_cn', 'thumbnail_image', 'publishedAt', 'show_youtube_url')
    list_editable = ['title_cn']
    readonly_fields = ('publishedAt',)
    list_per_page = 10
    search_fields = ('title', 'title_cn')



    def show_youtube_url(self, obj):
        return format_html("<a href='{youtube_url}' target='_blank'>{youtube_url}</a>",
                           youtube_url='https://www.youtube.com/watch?v=%s' % obj.video_id)

    show_youtube_url.allow_tags = True


admin.site.register(Video, VideoAdmin)