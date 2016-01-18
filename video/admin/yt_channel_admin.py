# coding=utf-8
from __future__ import unicode_literals

__author__ = 'GoTop'

from django.contrib import admin
from video.models import YT_channel

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

admin.site.register(YT_channel, YT_channelAdmin)