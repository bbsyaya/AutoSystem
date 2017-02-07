# coding=utf-8
from __future__ import unicode_literals
from django.template.loader import render_to_string
from django.utils.http import urlquote
from django.utils.safestring import mark_safe

__author__ = 'GoTop'

from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from video.models import Video, Youku
from video.forms import YoukuForm, VideoForm, VideoChangeListForm
from video.admin.video_admin_filter import DownloadFilter, UploadFilter, \
    DownloadUploadFilter


class YoukuInline(admin.StackedInline):
    model = Youku
    # add a custom inline admin widget in Django
    # http://stackoverflow.com/questions/433251/how-do-i-add-a-custom-inline
    # -admin-widget-in-django
    form = YoukuForm


class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'remark',
        # 'show_thumbnail',
        'published_at_readable',
        'show_duration_readable',
        'youtube_url',
        'show_video_of_channel',
        'show_video_of_playlist',
        'allow_upload_youku',
        'download_youtube_url',
        'download_subtitle_url',
        # 'merge_subtitle',
        'change_vtt_to_ass_and_edit_style',
        'merge_subtitle_to_video',
        'youku_url',
        'set_youku_playlist_online_from_config_playlist_url',
        'update_youku_online_url',
        'delete_youku_video_url',
        'download_upload_video_url',
    )
    list_editable = ['allow_upload_youku', 'remark']

    readonly_fields = ('title', 'description', 'thumbnail',
                       'publishedAt', 'youtube_url', 'duration_readable',
                       'view_count', 'channel',
                       'like_count', 'tags_readable')
    list_per_page = 20
    search_fields = ('title', 'video_id', 'channel__title')  # 只能是model中的text
    # field
    inlines = [YoukuInline, ]

    list_filter = [DownloadFilter, UploadFilter, DownloadUploadFilter,
                   'channel__is_download',
                   'channel__category',
                   'channel__title',
                   'playlist__title']

    # 设置在change和edit页面显示哪些field
    fieldsets = (
        ('Main', {
            # 'classes': ('wide',),
            'fields': (
                'title', 'youtube_url', 'publishedAt',
                'duration_readable',
                'tags_readable',
                'description',
                'thumbnail', 'channel', 'view_count', 'like_count',)
        }),
        ('Options', {
            # 'classes': ('wide',),
            'fields': (
                'allow_upload_youku',)
        }),
        ('Subtitles', {
            # 'classes': ('wide',),
            'fields': (
                'subtitle_en', 'subtitle_cn', 'subtitle_merge')

        }),
        ('Files', {
            # 'classes': ('wide',),
            'fields': (
                'file', 'subtitle_video_file',)
        }),
        ('Others', {
            'classes': ('collapse',),
            'fields': (
                'baidu_yun', 'remark')
        }),
    )

    # It is used to create the form presented on both the add/change pages.
    # 用来定义 add和change页面的表格
    form = VideoForm

    # form =VideoChangeListForm

    # 通过编写ModelAdmin类中的get_changelist_form()来自定义changelist 页面的form
    def get_changelist_form(self, request, **kwargs):
        return VideoChangeListForm

    # 使用什么字段来排序
    ordering = ('-publishedAt', 'title')

    # 设置使用select_related，在获取video的changelist页面直接获取video对象和其youku的值
    # 避免没一个video对象单独查询一次youku对象的信息
    list_select_related = (
        'youku', 'channel'
    )

    # 设置使用select_related，在获取video的changelist页面直接获取video对象和其youku的值
    # 避免没一个video对象单独查询一次youku对象的信息
    #
    # def queryset(self, request):
    #     return super(VideoAdmin, self).queryset(request).prefetch_related(
    #         'youku')

    # def get_form(self, request, obj=None, **kwargs):
    #     # Proper kwargs are form, fields, exclude, formfield_callback
    #     if obj: # obj is not None, so this is a change page
    #         kwargs['exclude'] = []
    #     else: # obj is None, so this is an add page
    #         kwargs['exclude'] = ['subtile_en', 'subtile_cn',]
    #     return super(VideoAdmin, self).get_form(request, obj, **kwargs)


    # 在changeform页面，不显示'title_cn'属性，一定要在‘title_cn’后加逗号
    # http://stackoverflow.com/a/31791675/1314124
    def changeform_view(self, request, object_id, form_url='',
                        extra_content=None):
        self.exclude = ('title_cn',)
        return super(VideoAdmin, self).changeform_view(request,
                                                       object_id)

    def show_thumbnail(self, obj):
        return '<img src="%s" width="50" height="50"/>' % obj.thumbnail

    show_thumbnail.allow_tags = True
    show_thumbnail.short_description = 'Thumbnail'

    def show_duration_readable(self, object):
        return object.duration_readable

    show_duration_readable.short_description = "时长"

    def published_at_readable(self, obj):
        # return obj.publishedAt.strftime("%Y-%m-%d %H:%M")
        return obj.publishedAt.strftime("%m-%d %H:%M")

    published_at_readable.short_description = '发布时间'

    def youtube_url(self, obj):
        youtube_url = 'https://www.youtube.com/watch?v=%s' % obj.video_id
        return "<a href='%s' target='_blank'>YouTube链接</a>" % youtube_url

    youtube_url.allow_tags = True
    youtube_url.short_description = 'YouTube'

    def show_video_of_channel(self, obj):
        if obj.channel:
            change_url = reverse('admin:video_video_changelist')
            extra = "?playlist__title__exact=%s" % (obj.channel.title)
            return "<a href='%s' target='_blank'>%s</a>" % \
                   (change_url + extra, obj.channel.title)
        else:
            return "-"

    show_video_of_channel.allow_tags = True
    show_video_of_channel.short_description = '频道'

    def show_video_of_playlist(self, obj):
        # video不一定有对应playlist
        if obj.playlist:
            change_url = reverse('admin:video_video_changelist')
            extra = "?playlist__title__exact=%s" % (obj.playlist.title)
            return "<a href='%s' target='_blank'>%s</a>" % \
                   (change_url + extra, obj.playlist.title)
        else:
            return "-"

    show_video_of_playlist.allow_tags = True
    show_video_of_playlist.short_description = '播单'

    def download_youtube_url(self, obj):
        if obj.file:
            view_file_url = "file:///" + urlquote(obj.file.path)
            return "<a href='%s' target='_blank'>文件-地址</a>" % view_file_url
        else:
            download_youtube_url = reverse(
                'video:download_single_youtube_video',
                args=[obj.video_id])
            return "<a href='%s' target='_blank'>下载</a>" % download_youtube_url

    download_youtube_url.allow_tags = True
    download_youtube_url.short_description = '下载YouTube'

    def download_subtitle_url(self, obj):
        if obj.subtitle_cn:
            return "<a href='%s' target='_blank'>字幕-地址</a>" % obj.subtitle_cn
        else:
            download_subtitle_url = reverse('video:download_subtitle',
                                            args=[obj.video_id])
            return "<a href='%s' target='_blank'>下载-字幕</a>" % \
                   download_subtitle_url

    download_subtitle_url.allow_tags = True
    download_subtitle_url.short_description = '下载字幕'

    def merge_subtitle(self, obj):
        if obj.subtitle_merge:
            return "<a href='%s' target='_blank'>双语字幕-地址</a>" % \
                   obj.subtitle_merge
        elif obj.subtitle_en and obj.subtitle_cn:
            merge_subtitle_url = reverse('video:merge_sub_edit_style',
                                         args=[obj.video_id])
            return "<a href='%s' target='_blank'>合并编辑式样-中英字幕</a>" % \
                   merge_subtitle_url
        else:
            return "-"

    merge_subtitle.allow_tags = True
    merge_subtitle.short_description = '合并中英字幕'

    def change_vtt_to_ass_and_edit_style(self, obj):
        if obj.subtitle_merge:
            return "<a href='%s' target='_blank'>式样字幕</a>" % \
                   obj.subtitle_merge
        elif obj.subtitle_cn:
            change_vtt_to_ass_and_edit_style_url = reverse(
                'video:change_vtt_to_ass_and_edit_style',
                args=[obj.video_id])
            return "<a href='%s' target='_blank'>生成式样字幕</a>" % \
                   change_vtt_to_ass_and_edit_style_url
        else:
            return "无cn字幕"

    change_vtt_to_ass_and_edit_style.allow_tags = True
    change_vtt_to_ass_and_edit_style.short_description = '式样字幕'

    def merge_subtitle_to_video(self, obj):
        if obj.subtitle_video_file:
            subtitle_video_file_url = "file:///" + urlquote(
                obj.subtitle_video_file.path)
            return "<a href='%s' target='_blank'>包含字幕视频-地址</a>" % \
                   subtitle_video_file_url
        elif obj.file and obj.subtitle_cn:
            merge_subtitle_to_video_url = reverse(
                'video:merge_subtitle_to_video',
                args=[obj.video_id, 'soft', 'merge'])
            return "<a href='%s' target='_blank'>合并式样字幕到视频</a>" % \
                   merge_subtitle_to_video_url
        else:
            return "-"

    merge_subtitle_to_video.allow_tags = True
    merge_subtitle_to_video.short_description = '合并式样字幕到视频'

    def youku_url(self, obj):
        # To check if the (OneToOne) relation exists or not, you can use the
        # hasattr function:
        # http://stackoverflow.com/questions/3463240/check-if-onetoonefield
        # -is-none-in-django
        if hasattr(obj, 'youku'):
            if obj.youku.youku_video_id != '':
                # 显示已经上传到优酷网站的视频链接
                youku_url = 'http://v.youku.com/v_show/id_%s.html' % \
                            obj.youku.youku_video_id
                return "<a href='%s' target='_blank'>优酷视频链接</a>" % youku_url
            else:
                # 显示上传video到优酷网站的链接
                publish_youku_url = reverse('video:youku_upload',
                                            args=[obj.youku.id])
                return "<a href='%s' target='_blank'>上传</a>" % publish_youku_url
        else:
            # 显示为video添加youku信息的链接，但是要手动设置youku对应的video，不实用
            publish_youku_url = reverse('admin:video_youku_add', )
            return "<a href='%s' target='_blank'>添加-优酷信息</a>" % \
                   publish_youku_url

    youku_url.allow_tags = True
    youku_url.short_description = '优酷视频链接'

    # def get_youku_video_info_url(self, obj):
    #     if hasattr(obj, 'youku'):
    #         # 如果已经有youku 视频的信息，则显示访问youku model的链接
    #         # if obj.youku.youku_video_id != '':
    #         #     # 如果 youku 对象的 youku_video_id 存在，则显示获取优酷视频信息的链接
    #         #     get_youku_video_info_url = reverse(
    # 'video:get_youku_video_info', args=[obj.youku.id])
    #         #     return "<a href='%s' target='_blank'>获取优酷在线信息</a>" %
    # get_youku_video_info_url
    #         # else:
    #         # 有发布优酷视频的信息，说明之前已经获取过，则显示访问youku model的链接
    #         # 参考 https://docs.djangoproject.com/en/1.7/ref/contrib/admin
    # /#reversing-admin-urls
    #         youku_video_info_change_url = reverse(
    # 'admin:video_youku_change', args=[obj.youku.id])
    #         return "<a href='%s' target='_blank'>本地youku对象信息</a>" %
    # youku_video_info_change_url
    #     else:
    #         # 如果还没有上传到优酷，则说明都不显示
    #         return "-"
    #
    # get_youku_video_info_url.allow_tags = True
    # get_youku_video_info_url.short_description = '获取优酷视频信息'

    def set_youku_playlist_online_from_config_playlist_url(self,obj):
        if hasattr(obj, 'youku'):
            # 如果youku对象有youku_video_id(说明视频已经上传到优酷)
            if obj.youku.youku_video_id != '':
                set_youku_playlist_online_from_config_playlist_url = reverse(
                    'video:set_youku_playlist_online_from_config_playlist',
                    args=[obj.video_id])

                return "<a href='%s' target='_blank'>设置优酷播单OL</a>" % \
                       set_youku_playlist_online_from_config_playlist_url
            else:
                return "-"
        else:
            return "-"
    set_youku_playlist_online_from_config_playlist_url.allow_tags = True
    set_youku_playlist_online_from_config_playlist_url.short_description = '设置优酷播单OL'


    def update_youku_online_url(self, obj):
        if hasattr(obj, 'youku'):
            if obj.youku.youku_video_id != '':
                edit_youku_url = reverse(
                    'video:update_youku_online_info',
                    args=[obj.youku.youku_video_id])
                return "<a href='%s' target='_blank'>更新优酷OL</a>" % \
                       edit_youku_url
            else:
                return "-"
        else:
            return "-"

    update_youku_online_url.allow_tags = True
    update_youku_online_url.short_description = '更新优酷OL'

    def delete_youku_video_url(self, obj):
        if hasattr(obj, 'youku'):
            if obj.youku.youku_video_id != '':
                delete_youku_video_url = reverse('video:delete_youku_video',
                                                 args=[
                                                     obj.youku.youku_video_id, ])
                return "<a href='%s' target='_blank'>Delete Youku</a>" % \
                       delete_youku_video_url
            else:
                return "-"
        else:
            return "-"

    delete_youku_video_url.allow_tags = True
    delete_youku_video_url.short_description = '删除优酷视频OL'

    def edit_youku_url(self, obj):
        if hasattr(obj, 'youku'):
            edit_youku_url = reverse('admin:video_youku_change',
                                     args=[obj.youku.id])
            return "<a href='%s' target='_blank'>Edit Youku</a>" % \
                   edit_youku_url
        else:
            edit_youku_url = reverse('admin:video_youku_add', )
            return "<a href='%s' target='_blank'>Add Youku</a>" % edit_youku_url

    edit_youku_url.allow_tags = True
    edit_youku_url.short_description = '修改优酷信息OL'

    def download_upload_video_url(self, obj):
        if hasattr(obj, 'youku'):
            if obj.youku.youku_video_id != '':
                # 如果youku_video_id不是空值，说明视频已经上传到优酷
                return "-"
            else:
                # video设置有对应的youku对象，但是youku.youku_video_id为空，说明没有上传到优酷
                download_upload_video_url = reverse(
                    'video:download_upload_video', args=[obj.video_id, ])
                return "<a href='%s' target='_blank'>下载+上传</a>" % \
                       download_upload_video_url
        else:
            download_upload_video_url = reverse(
                'video:download_upload_video', args=[obj.video_id, ])
            return "<a href='%s' target='_blank'>下载+上传</a>" % \
                   download_upload_video_url

    download_upload_video_url.allow_tags = True
    download_upload_video_url.short_description = '下载+上传'

    def save_formset(self, request, form, formset, change):
        """
        当Video Admin的页面保存inline对象(youku)时,如果更改了youku的playlist设置,
        则在playlist_id的优酷playlist中删除youku_video_id视频,
        并在优酷网上将视频添加到新设置的playlist中
        同时更新youku的playlist属性的值

        save_formset is called potentially many times during each add / change,
        once for every inline defined on your ModelAdmin.
        It is called by the base class implementation of save_related.

        form 为video的form
        formset是 inline对象 youku 的form

        :param request:
        :param form:
        :param formset:
        :param change:
        :return:
        """
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            # instance 为 youku 对象
            instance.save()
            if 'setted_youku_playlist' in formset.forms[0].changed_data:
                # 如果设置的setted_youku_playlist与youku_playlist不相同，则要在优酷网上将video
                # 从youku_playlist中删除，然后再将video添加到setted_youku_playlist中，
                # 最后将本地数据库中的youku_playlist设置为setted_youku_playlist
                setted_youku_playlist = formset.forms[0].cleaned_data[
                    'setted_youku_playlist']
                origin_youku_playlist = formset.forms[0].cleaned_data[
                    'youku_playlist']
                if setted_youku_playlist:
                    if setted_youku_playlist != origin_youku_playlist:
                        # todo 以下这段引用如果放在顶部则无法启动django server，原因未明
                        from video.function.youku_playlist import \
                            delete_video_from_playlist, \
                            set_youku_playlist_online
                        # 只要改变了field['youku_playlist']，自动在playlist_id的优酷playlist
                        # 中删除youku_video_id视频
                        if origin_youku_playlist:
                            delete_video_from_playlist(instance.youku_video_id,
                                                       origin_youku_playlist.id)
                        playlist_id = set_youku_playlist_online(
                            instance.youku_video_id, setted_youku_playlist.id)
                        if playlist_id:
                            instance.youku_playlist = \
                                instance.setted_youku_playlist
                            instance.save(update_fields=['youku_playlist'])
        formset.save_m2m()


admin.site.register(Video, VideoAdmin)
