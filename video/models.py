# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Video(models.Model):
    video_id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300, null=True, blank=True)
    publishedAt = models.DateTimeField(null=True, blank=True)
    thumbnail = models.URLField(max_length=300, null=True, blank=True)

    title_cn = models.CharField(max_length=50, null=True, blank=True)
    subtile_en = models.CharField(max_length=50, null=True, blank=True)
    subtile_cn = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to='youtube', null=True, blank=True)
    youku = models.ForeignKey('Youku', null=True, blank=True)
    baiduy_yun = models.ForeignKey('BaiduYun', null=True, blank=True)
    remark = models.CharField(max_length=300, null=True, blank=True)


    def __str__(self):
        return self.title

    def thumbnail_image(self):
        return '<img src="%s"/>' % self.thumbnail

    @property
    def youtube_url(self):
        return 'https://www.youtube.com/watch?v=%s' % self.video_id

    # youtube_url = property(_youtube_url)


    thumbnail_image.allow_tags = True


class YT_playlist(models.Model):
    """
    设置关注youtube的用户，或者
    """
    playlist_id = models.URLField(max_length=100, primary_key=True)
    remark = models.CharField(max_length=50)


class YT_channel():
    channel_id = models.URLField(max_length=100, primary_key=True)
    remark = models.CharField(max_length=50)


class YouTube(models.Model):
    """
    设置关注youtube的用户，或者
    """
    vid_id = models.CharField(max_length=50)
    vid_url = models.CharField(max_length=50)
    playlist_url = models.URLField(max_length=300)
    user = models.URLField(max_length=300)
    keywords = models.CharField(max_length=50)


class Youku(models.Model):
    video_id = models.CharField(max_length=50)


class BaiduYun(models.Model):
    uri = models.CharField(max_length=50)



