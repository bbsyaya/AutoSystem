# coding=utf-8
from __future__ import unicode_literals
from adminbrowse import AutoBrowseModelAdmin, link_to_url, link_to_changelist, link_to_change
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import Video, Youku


# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'title_cn', 'thumbnail_image', 'publishedAt', 'show_download_youtube_url', 'show_youtube_url',
        'show_youku_url', 'show_get_youku_video_info_url')
    list_editable = ['title_cn']
    readonly_fields = ('publishedAt',)
    list_per_page = 10
    search_fields = ('title', 'title_cn')

    def show_youtube_url(self, obj):
        youtube_url = 'https://www.youtube.com/watch?v=%s' % obj.video_id
        return "<a href='%s' target='_blank'>YouTube链接</a>" % youtube_url

    show_youtube_url.allow_tags = True
    show_youtube_url.short_description = 'YouTube'

    def show_download_youtube_url(self, obj):
        if obj.file:
            return obj.file
        else:
            download_youtube_url = reverse('video:download_single_youtube_video', args=[obj.video_id])
            return "<a href='%s' target='_blank'>下载</a>" % download_youtube_url

    show_download_youtube_url.allow_tags = True
    show_download_youtube_url.short_description = 'Download YouTube'

    def show_youku_url(self, obj):
        if obj.youku_id:
            youku_url = 'http://v.youku.com/v_show/id_%s.html' % obj.youku_id
            return "<a href='%s' target='_blank'>优酷链接</a>" % youku_url
        else:
            publish_youku_url = reverse('video:youku_upload', args=[obj.video_id])
            return "<a href='%s' target='_blank'>上传</a>" % publish_youku_url

    show_youku_url.allow_tags = True
    show_youku_url.short_description = '优酷'

    def show_get_youku_video_info_url(self, obj):
        if obj.youku_id:
            # 如果已经有youku 视频的信息，则显示访问youku model的链接
            youku = Youku.objects.get(video_id=obj.youku_id)
            if youku.published == None:
                # 如果没有youku 视频published的信息，则显示获取优酷视频信息的链接
                get_youku_video_info_url = reverse('video:get_youku_video_info', args=[obj.youku_id])
                return "<a href='%s' target='_blank'>获取信息</a>" % get_youku_video_info_url
            else:
                # 有发布优酷视频的信息，说明之前已经获取过，则显示访问youku model的链接
                # 参考 https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#reversing-admin-urls
                youku_video_info_change_url = reverse('admin:video_youku_change', args=[obj.youku_id])
                return "<a href='%s' target='_blank'>查看优酷视频信息</a>" % youku_video_info_change_url
        else:
            # 如果还没有上传到优酷，则说明都不显示
            return "-"

    show_get_youku_video_info_url.allow_tags = True
    show_get_youku_video_info_url.short_description = '获取优酷视频信息'


class YoukuAdmin(admin.ModelAdmin):
    pass


admin.site.register(Video, VideoAdmin)

admin.site.register(Youku, YoukuAdmin)
