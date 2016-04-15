# coding=utf-8
from __future__ import unicode_literals, absolute_import
from django.contrib import admin
from django.db.models import Q

__author__ = 'GoTop'


class DownloadFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = '是否下载视频文件'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'download'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('0', '未下载'),
            ('1', '已下载'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # 未下载
        if self.value() == '0':
            return queryset.filter(file='')
        # 已下载
        if self.value() == '1':
            # 设置了youku model，并且已下载youtube视频文件到本地
            return queryset.exclude(file='')


class UploadFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = '是否上传到优酷'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'upload'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('0', '设置了youku，但未上传'),
            ('1', '设置了youku，已上传'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # 未上传到youku,返回的对象都是设置了youku的video
        if self.value() == '0':
            return queryset.filter(youku__youku_video_id='')
        # 已上传到youku
        if self.value() == '1':
            # 设置了youku model，并且已下载youtube视频文件到本地
            # 使用queryset.filter(~Q(youku__youku_video_id = ''))
            # 或 exclude(youku__youku_video_id = '')都会使
            # django自动在SQL语句中加入"video_youku"."youku_video_id" IS NOT NULL
            # SQL语句是: WHERE NOT ("video_youku"."youku_video_id" = ''
            # AND "video_youku"."youku_video_id" IS NOT NULL)
            # 会获取youku_video_id不为'',或youku_video_id 是null的记录
            # 解决的方法是使用自定义lookup
            return queryset.filter(youku__youku_video_id__ne='')


class DownloadUploadFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = '下载上传'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'download_upload'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('0', '设置了youku，但未下载'),
            ('1', '已下载，但未上传'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # 设置了youku，但未下载
        if self.value() == '0':
            return queryset.filter(youku__isnull=False, file='')
        # 已下载，但未上传
        if self.value() == '1':
            # 设置了youku model，并且已下载youtube视频文件到本地
            return queryset.filter(youku__youku_video_id__ne='').exclude(
                file='')
