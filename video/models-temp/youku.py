# coding=utf-8
from __future__ import unicode_literals, absolute_import
from django.db import models
__author__ = 'GoTop'

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
    # youku_video_id 是视频上传到优酷的video id
    youku_video_id = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=50, blank=True,
                            help_text="自定义标签不超过10个，单个标签最少2个字符，最多12个字符（6个汉字），多个标签之间用逗号(,)隔开"
                            )
    description = models.TextField(max_length=300, blank=True, default='')
    category = models.CharField(max_length=50, blank=True, choices=YOUKU_PALYLIST_CATEGORY)
    published = models.DateTimeField(null=True, blank=True)
    # on_delete=models.SET_NULL 表示如果对应的Video被删除，Youku只将个属性设置为null，不会删除youku对象
    # OneToOneField要设置在 要被显示在inline的model里
    # 参考 http://stackoverflow.com/questions/1744203/django-admin-onetoone-relation-as-an-inline
    # 指向video model，所以youku model会有一个video id属性，注意与youku_video_id的区别
    video = models.OneToOneField('Video', on_delete=models.SET_NULL, null=True, blank=True)
    youku_playlist = models.ForeignKey('YoukuPlaylist', on_delete=models.SET_NULL, null=True, blank=True)


    @property
    def url(self):
        url = 'http://v.youku.com/v_show/id_' + self.youku_video_id + '.html'
        return url

    def __str__(self):
        return self.youku_video_id