# coding=utf-8
from __future__ import unicode_literals

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

__author__ = 'GoTop'

from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse

from video.models import Video, Youku
from video.forms import YoukuForm, VideoForm


class YoukuInline(admin.StackedInline):
    model = Youku
    # add a custom inline admin widget in Django
    # http://stackoverflow.com/questions/433251/how-do-i-add-a-custom-inline-admin-widget-in-django
    form = YoukuForm


class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'title_cn', 'show_thumbnail', 'publishedAt', 'download_youtube_url', 'youtube_url', 'merge_subtitle',
        'youku_url', 'get_youku_video_info_url', 'update_youku_online_url')
    list_editable = ['title_cn']
    readonly_fields = ('publishedAt',)
    list_per_page = 10
    search_fields = ('title', 'title_cn')
    inlines = [
        YoukuInline,
    ]

    form = VideoForm
    ordering = ('-publishedAt', 'title')

    # def get_form(self, request, obj=None, **kwargs):
    #     # Proper kwargs are form, fields, exclude, formfield_callback
    #     if obj: # obj is not None, so this is a change page
    #         kwargs['exclude'] = []
    #     else: # obj is None, so this is an add page
    #         kwargs['exclude'] = ['subtile_en', 'subtile_cn',]
    #     return super(VideoAdmin, self).get_form(request, obj, **kwargs)


    # 在changeform页面，不显示'title_cn'属性，一定要在‘title_cn’后加逗号
    # http://stackoverflow.com/a/31791675/1314124
    def changeform_view(self, request, object_id, form_url='', extra_content=None):
        self.exclude = ('title_cn',)
        return super(VideoAdmin, self).changeform_view(request, object_id)

    def show_thumbnail(self, obj):
        return '<img src="%s" width="50" height="50"/>' % obj.thumbnail

    show_thumbnail.allow_tags = True
    show_thumbnail.short_description = 'Thumbnail'

    def youtube_url(self, obj):
        youtube_url = 'https://www.youtube.com/watch?v=%s' % obj.video_id
        return "<a href='%s' target='_blank'>YouTube链接</a>" % youtube_url

    youtube_url.allow_tags = True
    youtube_url.short_description = 'YouTube'

    def download_youtube_url(self, obj):
        if obj.file:
            return obj.file
        else:
            download_youtube_url = reverse('video:download_single_youtube_video', args=[obj.video_id])
            return "<a href='%s' target='_blank'>下载</a>" % download_youtube_url

    download_youtube_url.allow_tags = True
    download_youtube_url.short_description = 'Download YouTube'

    def merge_subtitle(self, obj):

        merge_subtitle_url = reverse('video:merge_subtitle', args=[obj.video_id])
        return "<a href='%s' target='_blank'>合并中英字幕</a>" % merge_subtitle_url

    merge_subtitle.allow_tags = True
    merge_subtitle.short_description = '合并中英字幕'

    def youku_url(self, obj):
        # To check if the (OneToOne) relation exists or not, you can use the hasattr function:
        # http: // stackoverflow.com / questions / 3463240 / check - if -onetoonefield - is -none - in -django
        if hasattr(obj, 'youku'):
            if obj.youku.youku_video_id != '':
                # 显示已经上传到优酷网站的视频链接
                youku_url = 'http://v.youku.com/v_show/id_%s.html' % obj.youku.youku_video_id
                return "<a href='%s' target='_blank'>优酷网视频链接</a>" % youku_url
            else:
                # 显示上传video到优酷网站的链接
                publish_youku_url = reverse('video:youku_upload', args=[obj.youku.id])
                return "<a href='%s' target='_blank'>上传</a>" % publish_youku_url
        else:
            # 显示为video添加youku信息的链接
            publish_youku_url = reverse('admin:video_youku_add', )
            return "<a href='%s' target='_blank'>上传</a>" % publish_youku_url

    youku_url.allow_tags = True
    youku_url.short_description = '优酷网视频链接'

    def get_youku_video_info_url(self, obj):
        if hasattr(obj, 'youku'):
            # 如果已经有youku 视频的信息，则显示访问youku model的链接
            # if obj.youku.youku_video_id != '':
            #     # 如果 youku 对象的 youku_video_id 存在，则显示获取优酷视频信息的链接
            #     get_youku_video_info_url = reverse('video:get_youku_video_info', args=[obj.youku.id])
            #     return "<a href='%s' target='_blank'>获取优酷在线信息</a>" % get_youku_video_info_url
            # else:
            # 有发布优酷视频的信息，说明之前已经获取过，则显示访问youku model的链接
            # 参考 https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#reversing-admin-urls
            youku_video_info_change_url = reverse('admin:video_youku_change', args=[obj.youku.id])
            return "<a href='%s' target='_blank'>查看本地youku对象信息</a>" % youku_video_info_change_url
        else:
            # 如果还没有上传到优酷，则说明都不显示
            return "-"

    get_youku_video_info_url.allow_tags = True
    get_youku_video_info_url.short_description = '获取优酷视频信息'

    def update_youku_online_url(self, obj):
        if hasattr(obj, 'youku'):
            if obj.youku.youku_video_id != '':
                edit_youku_url = reverse('video:update_youku_online_info', args=(obj.youku.youku_video_id,))
                return "<a href='%s' target='_blank'>更新优酷网信息</a>" % edit_youku_url
            else:
                return "-"
        else:
            return "-"

    update_youku_online_url.allow_tags = True
    update_youku_online_url.short_description = '更新优酷网信息'

    def edit_youku_url(self, obj):
        if hasattr(obj, 'youku'):
            edit_youku_url = reverse('admin:video_youku_change', args=(obj.youku.id,))
            return "<a href='%s' target='_blank'>Edit Youku</a>" % edit_youku_url
        else:
            edit_youku_url = reverse('admin:video_youku_add', )
            return "<a href='%s' target='_blank'>Add Youku</a>" % edit_youku_url

    edit_youku_url.allow_tags = True
    edit_youku_url.short_description = '修改优酷信息'


admin.site.register(Video, VideoAdmin)
