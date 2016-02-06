# coding=utf-8
from __future__ import unicode_literals, absolute_import
from django.db import models

from video.models import YT_channel

__author__ = 'GoTop'


class SetYoukuInfoManager(models.Manager):
    def get_queryset(self):
        return super(SetYoukuInfoManager, self).get_queryset().filter(youku__isnull=False)

class DownloadedManager(models.Manager):
    def get_queryset(self):
        return super(DownloadedManager, self).get_queryset().filter(file__isnull=False)


class Video(models.Model):
    video_id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=200, )
    description = models.TextField(max_length=300, blank=True)
    publishedAt = models.DateTimeField(null=True, blank=True)
    thumbnail = models.URLField(max_length=300, blank=True)
    channel = models.ForeignKey(YT_channel, null=True, blank=True)

    title_cn = models.CharField(max_length=100, blank=True)
    subtitle_en = models.CharField(max_length=100, blank=True)
    subtitle_cn = models.CharField(max_length=100, blank=True)
    subtitle_merge = models.CharField(max_length=100, blank=True, null=True)

    # The exception is CharFields and TextFields, which in Django are never saved as NULL.
    #  Blank values are stored in the DB as an empty string ('').
    # Avoid using null on string-based fields such as CharField and TextField because empty string values will always
    #  be stored as empty strings, not as NULL. If a string-based field has null=True, that means it has two possible
    #  values for "no data": NULL, and the empty string. In most cases, it’s redundant to have two possible values
    # for "no data"; the Django convention is to use the empty string, not NULL.
    file = models.CharField(max_length=100, blank=True)
    # youku = models.ForeignKey('Youku', null=True, blank=True)
    subtitle_video_file = models.CharField(max_length=100, blank=True, null=True)
    #baidu_yun = models.ForeignKey('BaiduYun', null=True, blank=True)
    remark = models.CharField(max_length=300, blank=True)

    object = models.Manager()
    set_youku = SetYoukuInfoManager()
    downloaded = DownloadedManager()


    def __str__(self):
        return self.title

    def thumbnail_image(self):
        return '<img src="%s"/>' % self.thumbnail

    @property
    def youtube_url(self):
        return 'https://www.youtube.com/watch?v=%s' % self.video_id

        # youtube_url = property(_youtube_url)
