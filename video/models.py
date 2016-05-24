# coding=utf-8
from __future__ import unicode_literals

import json
import re

from django import forms
from django.db import models

from django.db.models import Lookup
from django.db.models.fields import Field


class NeedUploadManager(models.Manager):
    def get_queryset(self):
        # 返回Video model中 allow_upload_youku为true，设置有对应的youku model，
        # 已下载视频文件过，并且未上传到优酷网(youku__youku_video_id='')的video
        need_upload_queryset = super(NeedUploadManager,
                                     self).get_queryset().filter(
            # 在SQLite数据库中，django model BooleanField True对应1，False对应0
            # 不知道在Django1.7之后的版本是否修改该bug
            allow_upload_youku=1,
            youku__isnull=False,
            youku__youku_video_id='').exclude(file='')

        return need_upload_queryset


class NeedDownloadUploadManager(models.Manager):
    def get_queryset(self):
        # 返回Video model中 allow_upload_youku为true，设置有对应的youku model，
        # 未下载视频文件过，并且未上传到优酷网(youku__youku_video_id='')的video
        # 注意：该函数不返回已经上传到youku，但是file文件被删除（为空）的video
        # （被自动清理函数删除了），以免重复下载
        need_download_upload_queryset = super(NeedDownloadUploadManager,
                                              self).get_queryset().filter(
            # 在SQLite数据库中，django model BooleanField True对应1，False对应0
            # 不知道在Django1.7之后的版本是否修改该bug
            allow_upload_youku=1,
            file='',
            youku__isnull=False,
            youku__youku_video_id='')

        return need_download_upload_queryset


class NeedGetVideoInfoManager(models.Manager):
    # 返回video model中视频时长为空的video
    def get_queryset(self):
        need_get_video_info_queryset = super(NeedGetVideoInfoManager,
                                             self).get_queryset().filter(
            duration=None)

        return need_get_video_info_queryset


class DownloadedManager(models.Manager):
    """
    获取未下载过视频文件的youtube video对象
    """

    def get_queryset(self):
        return super(DownloadedManager, self).get_queryset().exclude(
            file='')


# Create your models here.
class Video(models.Model):
    # id = models.CharField(max_length=50, null=True, blank=True)
    video_id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=200, )
    description = models.TextField(max_length=300, blank=True)
    publishedAt = models.DateTimeField(null=True, blank=True)
    thumbnail = models.URLField(max_length=300, blank=True)
    channel = models.ForeignKey('YouTubeChannel', null=True, blank=True)

    view_count = models.CharField(max_length=10, blank=True)
    like_count = models.CharField(max_length=10, blank=True)
    tags = models.TextField(max_length=200, blank=True)
    duration = models.IntegerField(blank=True, null=True,
                                   help_text='视频时长，单位是s')

    # title_cn = models.CharField(max_length=150, blank=True)

    subtitle_en = models.FileField(max_length=200, blank=True, default='')
    subtitle_cn = models.FileField(max_length=200, blank=True, default='')
    subtitle_merge = models.FileField(max_length=200, blank=True, default='')

    # The exception is CharFields and TextFields, which in Django are never
    # saved as NULL.
    #  Blank values are stored in the DB as an empty string ('').
    # Avoid using null on string-based fields such as CharField and TextField
    #  because empty string values will always
    #  be stored as empty strings, not as NULL. If a string-based field has
    # null=True, that means it has two possible
    #  values for "no data": NULL, and the empty string. In most cases,
    # it’s redundant to have two possible values
    # for "no data"; the Django convention is to use the empty string, not NULL.
    file = models.FileField(max_length=200, blank=True, default='')
    subtitle_video_file = models.FileField(max_length=200, blank=True,
                                           default='')
    allow_upload_youku = models.BooleanField(blank=True, default='True',
                                             verbose_name="是否上传",
                                             help_text='是否可以上传到优酷，默认为True')
    baidu_yun = models.ForeignKey('BaiduYun', null=True, blank=True)
    remark = models.CharField(verbose_name="优酷标题", max_length=300, blank=True)

    def __str__(self):
        return self.title

    def thumbnail_image(self):
        return '<img src="%s"/>' % self.thumbnail

    @property
    def youtube_url(self):
        return 'https://www.youtube.com/watch?v=%s' % self.video_id

    @property
    def tags_readable(self):
        # 将list格式的tags转化为用逗号分隔形式是string
        if self.tags:
            jsonDec = json.decoder.JSONDecoder()
            tags_list = jsonDec.decode(self.tags)
            return ', '.join(tags_list)
        else:
            return self.tags

    @property
    def duration_readable(self):
        # 以分，秒的形式，返回视频时长
        if self.duration:
            m, s = divmod(self.duration, 60)
            if m:
                return "%s:%s" % (m, s)
            else:
                return "%s" % s
        else:
            return self.duration

    def get_tags(self, num):
        """
        返回指定个数num的tags的字符串，用，分割
        :param num:
        :return:
        """
        # 将list格式的tags转化为用逗号分隔形式是string
        # 对于没有tag的youtube video，下载该视频信息是会将null保存到video model的tag field中
        if self.tags and self.tags != 'null':
            jsonDec = json.decoder.JSONDecoder()
            tags_list = jsonDec.decode(self.tags)

            tags_fomart_list = []
            for tag in tags_list:
                # 优酷的单个tag中，不允许有 空格，下划线，减号, 点, &
                # 除了中文和英文字母以外的符号都不行
                # 优酷用英文逗号和空格来分割tags，如果单个tag中存在空格，
                # 可能会导致最终的tag数超过10个
                # tag = tag.replace(" ", "")
                # tag = tag.replace("-", "")
                # tag = tag.replace("_", "")
                # tag = tag.replace(".", "")
                # tag = tag.replace("+", "")
                # tag = tag.replace("&", "")

                # 替换掉 汉字、英文以外的所有字符
                # http://blog.csdn.net/liuqian1104/article/details/8134293
                tag = re.sub(ur"[^\u4e00-\u9fa5a-zA-Z0-9]", "", tag)
                # 上传到优酷时，单个tag最多20个字符，所以剔除超过20个字符的tag
                if len(tag) <= 20:
                    tags_fomart_list.append(tag)

            # 如果要获取的tags数num比tags中包含的词组要少，则截取tags_list中的num个tags
            if len(tags_fomart_list) > num:
                tags_fomart_list = tags_fomart_list[:num]

            # 上传时优酷用英文逗号和空格来分割tags
            return ','.join(tags_fomart_list)
        else:
            return False

    def delete_associate_video(self):
        """
        在硬盘上删除该video所有相关的视频，字幕文件
        并将video的相关field清零
        :return:
        """
        self.file.delete()
        self.subtitle_en.delete()
        self.subtitle_cn.delete()
        self.subtitle_merge.delete()
        self.subtitle_video_file.delete()

    objects = models.Manager()
    need_download_upload = NeedDownloadUploadManager()
    need_upload = NeedUploadManager()
    downloaded = DownloadedManager()
    need_get_video_info = NeedGetVideoInfoManager()


class YouTubeChannel(models.Model):
    channel_id = models.URLField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    thumbnail = models.URLField(max_length=300, blank=True)
    category = models.ForeignKey('Category', null=True, blank=True)
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


class YouTubePlaylist(models.Model):
    playlist_id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=50)
    description =  models.TextField(max_length=500, blank=True)
    thumbnail = models.URLField(max_length=300, blank=True)
    publishedAt = models.DateTimeField(null=True, blank=True)
    channel = models.ForeignKey('YouTubeChannel', null=True,
                                        blank=True)
    remark = models.CharField(max_length=50, blank=True)

    @property
    def url(self):
        url = 'https://www.youtube.com/playlist?list=' + self.channel_id
        return url

    def thumbnail_image(self):
        return '<img src="%s"/>' % self.thumbnail

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'YouTube Playlist'
        verbose_name_plural = 'YouTube Playlists'


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
# 优酷上对视频的分类代码
YOUKU_CATEGORY = (
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
    # 主键的名称为 id
    # youku_video_id 是视频上传到优酷的video id
    youku_video_id = models.CharField(max_length=50, blank=True)
    # 说明 doc.open.youku.com/?docid=393
    title = models.CharField(max_length=100, blank=True,
                             help_text='视频标题，能填写2-50个字符,上传时必选')
    tags = models.TextField(max_length=200, blank=True,
                            help_text="不超过10个;单个标签最少2个、最多12个字符;标签间用英文的逗号(,"
                                      ")和空格隔开，单个tag中，不允许有_ - ;必选")
    description = models.TextField(max_length=300, blank=True, default='',
                                   help_text='视频描述，最多能写2000个字')
    category = models.CharField(max_length=50, blank=True,
                                choices=YOUKU_CATEGORY)
    published = models.DateTimeField(null=True, blank=True)
    # on_delete=models.SET_NULL 表示如果对应的Video被删除，Youku只将个属性设置为null，不会删除youku对象
    # OneToOneField要设置在 要被显示在inline的model里
    # 参考 http://stackoverflow.com/questions/1744203/django-admin-onetoone
    # -relation-as-an-inline
    # 指向video model，所以youku model会有一个video id属性，注意与youku_video_id的区别
    video = models.OneToOneField('Video', on_delete=models.SET_NULL, null=True,
                                 blank=True)

    setted_youku_playlist = models.ForeignKey('YoukuPlaylist',
                                              related_name='setted_youku_playlist',
                                              on_delete=models.SET_NULL,
                                              null=True,
                                              blank=True, help_text=
                                              "设置该视频所属的Playlist")
    youku_playlist = models.ForeignKey('YoukuPlaylist',
                                       related_name='youku_playlist_online',
                                       on_delete=models.SET_NULL, null=True,
                                       blank=True,
                                       help_text=
                                       "该视频在优酷网上实际上的Playlist")

    @property
    def url(self):
        url = 'http://v.youku.com/v_show/id_' + self.youku_video_id + '.html'
        return url

    @property
    def tags_readable(self, num=999):
        """
        将list格式的tags转化为用逗号分隔形式是string
        :param num:
        :return:
        """
        tags_list = self.get_tags_list(num)

        if tags_list:
            return ', '.join(tags_list)
        else:
            return None

    def get_tags_list(self, num=999):
        """
        以list的形式，返回指定数量的tags
        :param num:默认为999，既不设置的时候返回所有的tags
        :return:
        """
        if self.tags:
            if len(self.tags) > num:
                # 如果tags的数量大于10，则只取前num个
                self.tags = self.tags[:num]
            jsonDec = json.decoder.JSONDecoder()
            # self.tags 用json形式保存
            tags_list = jsonDec.decode(self.tags)
            return tags_list
        else:
            return None

    def add_tags(self, tags_list):
        """
        将list形式的tags,加入到原tags字段中，再转化为json格式保存到tags字段
        :param tags_list:
        :return:
        """
        origin_tags_list = self.get_tags_list(num=999)

        self.tags = json.dumps(origin_tags_list + tags_list)
        self.save(update_fields=['tags'])

    def __str__(self):
        return self.youku_video_id


class YoukuPlaylist(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    link = models.CharField(max_length=100, blank=True, null=True)
    play_link = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    video_count = models.CharField(max_length=10, blank=True, null=True)
    view_count = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class BaiduYun(models.Model):
    uri = models.CharField(max_length=50)


class Category(models.Model):
    # Youtube的Channel的分类，设置有对应的youku_playlist的分类（优酷网站上的规定）
    title = models.CharField(max_length=50, blank=True)
    youku_playlist_category = models.CharField(max_length=50, blank=True,
                                               choices=YOUKU_CATEGORY,
                                               default="Others",
                                               help_text="对应的youku_playlist的分类")
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class VideoConfig(models.Model):
    # 自动下载指定playlist的youtube视频后上传到youku，并设置到指定playlist的相关配置
    youtube_channel = models.ForeignKey('YouTubeChannel',
                                        on_delete=models.SET_NULL, null=True,
                                        blank=True,
                                        help_text=
                                        "指定下载youtube上的指定channel")

    youtube_playlist = models.ForeignKey('YouTubePlaylist',
                                         # related_name='youku_playlist_online',
                                         on_delete=models.SET_NULL, null=True,
                                         blank=True,
                                         help_text=
                                         "指定下载youtube channel里的特定playlist")

    youku_account = models.CharField(max_length=100, blank=True,
                                     help_text=
                                     "指定上传到优酷的账号")

    youku_playlist = models.ForeignKey('YoukuPlaylist',
                                       on_delete=models.SET_NULL, null=True,
                                       blank=True,
                                       help_text=
                                       "设置视频在优酷网上的Playlist")
    is_enable = models.BooleanField(blank=True)
    remark = models.CharField(verbose_name="备注", max_length=300, blank=True)


@Field.register_lookup
class NotEqualLookup(Lookup):
    lookup_name = 'ne'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params
