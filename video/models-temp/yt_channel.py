# coding=utf-8
from __future__ import unicode_literals, absolute_import
from django.db import models

__author__ = 'GoTop'

class YT_channel(models.Model):
    channel_id = models.URLField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    thumbnail = models.URLField(max_length=300, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    is_download = models.NullBooleanField(null=True, blank=True)
    remark = models.CharField(max_length=50, blank=True)

    @property
    def url(self):
        url = 'https://www.youtube.com/channel/' + self.channel_id
        return url

    def thumbnail_image(self):
        return '<img src="%s"/>' % self.thumbnail

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'YouTube Channel'
        verbose_name_plural = 'YouTube Channels'
