# coding=utf-8
from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Video(models.Model):
    video_id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, null=True, blank=True)
    publishedAt = models.DateTimeField(null=True, blank=True)
    thumbnail = models.URLField(max_length=300, null=True, blank=True)

    title_cn = models.CharField(max_length=100, null=True, blank=True)
    subtile_en = models.CharField(max_length=50, null=True, blank=True)
    subtile_cn = models.CharField(max_length=50, null=True, blank=True)
    file = models.CharField(max_length=100, null=True, blank=True)
    # youku = models.ForeignKey('Youku', null=True, blank=True)

    baidu_yun = models.ForeignKey('BaiduYun', null=True, blank=True)
    remark = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title

    def thumbnail_image(self):
        return '<img src="%s"/>' % self.thumbnail

    @property
    def youtube_url(self):
        return 'https://www.youtube.com/watch?v=%s' % self.video_id

        # youtube_url = property(_youtube_url)


class YT_channel(models.Model):
    channel_id = models.URLField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300, null=True, blank=True)
    thumbnail = models.URLField(max_length=300, null=True, blank=True)
    category = models.ForeignKey('Category', null=True, blank=True)
    is_download = models.NullBooleanField(null=True, blank=True)
    remark = models.CharField(max_length=50)

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


class YouTube(models.Model):
    """
    设置关注youtube的用户，或者
    """
    vid_id = models.CharField(max_length=50)
    vid_url = models.CharField(max_length=50)
    playlist_url = models.URLField(max_length=300)
    user = models.URLField(max_length=300)
    keywords = models.CharField(max_length=50)


# http://cloud.youku.com/docs?id=90
YOUKU_PALYLIST_CATEGORY = (
    ("Games", "游戏"),
    ("Tech", "科技"),
    ("News", "资讯"),
    ("LifeStyle", "生活"),
    ("Original", "原创"),
    ("TV", "电视剧"),
    ("Entertainment", "娱乐"),
    ("Movies", "电影"),
    ("Sports", "体育"),
    ("Music", "音乐"),
    ("Anime", "动漫"),
    ("Fashion", "时尚"),
    ("Parenting", "亲子"),
    ("Autos", "汽车"),
    ("Travel", "旅游"),
    ("Education", "教育"),
    ("Humor", "搞笑"),
    ("Ads", "广告"),
    ("Others", "其他"),
)


class Youku(models.Model):
    youku_video_id = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    tags = models.CharField(max_length=50, null=True, blank=True,
                            help_text="自定义标签不超过10个，单个标签最少2个字符，最多12个字符（6个汉字），多个标签之间用逗号(,)隔开"
                            )
    description = models.CharField(max_length=300, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True, choices=YOUKU_PALYLIST_CATEGORY,
                                default="Others")
    published = models.DateTimeField(null=True, blank=True)
    # on_delete=models.SET_NULL 表示如果对应的Video被删除，Youku只将个属性设置为null，不会删除youku对象
    # OneToOneField要设置在 要被显示在inline的model里
    # 参考 http://stackoverflow.com/questions/1744203/django-admin-onetoone-relation-as-an-inline
    video = models.OneToOneField('Video', on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def url(self):
        url = 'http://v.youku.com/v_show/id_' + self.video_id + '.html'
        return url

    def __str__(self):
        return self.youku_video_id


class BaiduYun(models.Model):
    uri = models.CharField(max_length=50)


class Category(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title
