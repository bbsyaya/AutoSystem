# coding=utf-8
from __future__ import unicode_literals
from adminbrowse import AutoBrowseModelAdmin, link_to_url, link_to_changelist, link_to_change
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import Video, Youku, YT_channel, Category, BaiduYun


# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'title_cn', 'show_thumbnail', 'publishedAt', 'show_download_youtube_url', 'show_youtube_url',
        'show_youku_url', 'show_get_youku_video_info_url', 'edit_youku_url')
    list_editable = ['title_cn']
    readonly_fields = ('publishedAt',)
    list_per_page = 10
    search_fields = ('title', 'title_cn')

    ordering = ('-publishedAt', 'title')

    def show_thumbnail(self, obj):
        return '<img src="%s" width="50" height="50"/>' % obj.thumbnail

    show_thumbnail.allow_tags = True
    show_thumbnail.short_description = 'Thumbnail'

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
        if obj.youku:
            youku_url = 'http://v.youku.com/v_show/id_%s.html' % obj.youku.video_id
            return "<a href='%s' target='_blank'>优酷链接</a>" % youku_url
        else:
            publish_youku_url = reverse('video:youku_upload', args=[obj.video_id])
            return "<a href='%s' target='_blank'>上传</a>" % publish_youku_url

    show_youku_url.allow_tags = True
    show_youku_url.short_description = '优酷'

    def show_get_youku_video_info_url(self, obj):
        if obj.youku:
            # 如果已经有youku 视频的信息，则显示访问youku model的链接
            youku = Youku.objects.get(video_id=obj.youku.video_id)
            if youku.published == None:
                # 如果没有youku 视频published的信息，则显示获取优酷视频信息的链接
                get_youku_video_info_url = reverse('video:get_youku_video_info', args=[obj.youku.video_id])
                return "<a href='%s' target='_blank'>获取信息</a>" % get_youku_video_info_url
            else:
                # 有发布优酷视频的信息，说明之前已经获取过，则显示访问youku model的链接
                # 参考 https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#reversing-admin-urls
                youku_video_info_change_url = reverse('admin:video_youku_change', args=[obj.youku])
                return "<a href='%s' target='_blank'>查看优酷视频信息</a>" % youku_video_info_change_url
        else:
            # 如果还没有上传到优酷，则说明都不显示
            return "-"

    show_get_youku_video_info_url.allow_tags = True
    show_get_youku_video_info_url.short_description = '获取优酷视频信息'

    def edit_youku_url(self, obj):
        if obj.youku:
            edit_youku_url = reverse('admin:video_youku_change', args=(obj.youku_id,))
            return '<a href="%s">Edit Youku</a>' % edit_youku_url
        else:
            edit_youku_url = reverse('admin:video_youku_add', )
            return '<a href="%s">Add Youku</a>' % edit_youku_url
            return "-"

    edit_youku_url.allow_tags = True
    edit_youku_url.short_description = '修改优酷信息'


class YoukuAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class YT_channelAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_channel_url', 'show_thumbnail', 'description', 'category', 'is_download',
                    'remark')
    list_editable = ('is_download', 'category')
    list_per_page = 50
    search_fields = ('title',)
    list_filter = ('is_download', 'category')

    def show_channel_url(self, obj):
        return "<a href='%s' target='_blank'>频道Url</a>" % obj.url

    show_channel_url.allow_tags = True
    show_channel_url.short_description = 'Url'

    def show_thumbnail(self, obj):
        return '<img src="%s" width="50" height="50"/>' % obj.thumbnail

    show_thumbnail.allow_tags = True
    show_thumbnail.short_description = 'Thumbnail'

    # def show_category_url(self, obj):
    #     if obj.category_id:
    #         # 如果已经有 category_id 视频的信息，则显示访问 Category model的链接
    #         category = YT_channel.objects.get(category_id=obj.category_id)
    #         if category:
    #             # 参考 https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#reversing-admin-urls
    #             category_change_url = reverse('admin:video_category_change', args=[obj.category_id])
    #             return "<a href='%s' target='_blank'>%s</a>" % (category_change_url, category.title)
    #     else:
    #         # 参考 https://docs.djangoproject.com/en/1.7/ref/contrib/admin/#reversing-admin-urls
    #         category_change_url = reverse('admin:video_category_changelist')
    #         return "<a href='%s' target='_blank'></a>" % category_change_url
    #
    # show_category_url.allow_tags = True
    # show_category_url.short_description = 'Category'


admin.site.register(Video, VideoAdmin)
admin.site.register(Youku, YoukuAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(YT_channel, YT_channelAdmin)


class BaiduYunAdmin(admin.ModelAdmin):
    pass


admin.site.register(BaiduYun, BaiduYunAdmin)

