# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=50)
    url = models.URLField(max_length=300)
    title_cn = models.CharField(max_length=50)
    subtile_en = models.CharField(max_length=50)
    subtile_cn = models.CharField(max_length=50)
    youku = models.ForeignKey('Youku', null=True, blank=True)
    baiduy_yun = models.ForeignKey('BaiduYun', null=True, blank=True)

    remark = models.CharField(max_length=300, null=True, blank=True)



    def __str__(self):
        return self.title

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



