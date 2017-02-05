# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaiduYun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uri', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, blank=True)),
                ('youku_playlist_category', models.CharField(default='Others', help_text='\u5bf9\u5e94\u7684youku_playlist\u7684\u5206\u7c7b', max_length=50, blank=True, choices=[('Games', '\u6e38\u620f'), ('Tech', '\u79d1\u6280'), ('News', '\u8d44\u8baf'), ('LifeStyle', '\u751f\u6d3b'), ('Original', '\u539f\u521b'), ('TV', '\u7535\u89c6\u5267'), ('Entertainment', '\u5a31\u4e50'), ('Movies', '\u7535\u5f71'), ('Sports', '\u4f53\u80b2'), ('Music', '\u97f3\u4e50'), ('Anime', '\u52a8\u6f2b'), ('Fashion', '\u65f6\u5c1a'), ('Parenting', '\u4eb2\u5b50'), ('Autos', '\u6c7d\u8f66'), ('Travel', '\u65c5\u6e38'), ('Education', '\u6559\u80b2'), ('Humor', '\u641e\u7b11'), ('Ads', '\u5e7f\u544a'), ('Others', '\u5176\u4ed6')])),
                ('description', models.CharField(max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('youku_account', models.CharField(help_text='\u6307\u5b9a\u4e0a\u4f20\u5230\u4f18\u9177\u7684\u8d26\u53f7', max_length=100, blank=True)),
                ('is_enable', models.BooleanField()),
                ('remark', models.CharField(max_length=300, verbose_name='\u5907\u6ce8', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('video_id', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=300, blank=True)),
                ('publishedAt', models.DateTimeField(null=True, blank=True)),
                ('thumbnail', models.URLField(max_length=300, blank=True)),
                ('view_count', models.CharField(max_length=10, blank=True)),
                ('like_count', models.CharField(max_length=10, blank=True)),
                ('tags', models.TextField(max_length=200, blank=True)),
                ('duration', models.IntegerField(help_text='\u89c6\u9891\u65f6\u957f\uff0c\u5355\u4f4d\u662fs', null=True, blank=True)),
                ('subtitle_en', models.FileField(default='', max_length=200, upload_to=b'', blank=True)),
                ('subtitle_cn', models.FileField(default='', max_length=200, upload_to=b'', blank=True)),
                ('subtitle_merge', models.FileField(default='', max_length=200, upload_to=b'', blank=True)),
                ('file', models.FileField(default='', max_length=200, upload_to=b'', blank=True)),
                ('subtitle_video_file', models.FileField(default='', max_length=200, upload_to=b'', blank=True)),
                ('allow_upload_youku', models.BooleanField(default='True', help_text='\u662f\u5426\u53ef\u4ee5\u4e0a\u4f20\u5230\u4f18\u9177\uff0c\u9ed8\u8ba4\u4e3aTrue', verbose_name='\u662f\u5426\u4e0a\u4f20')),
                ('remark', models.CharField(max_length=300, verbose_name='\u4f18\u9177\u6807\u9898', blank=True)),
                ('baidu_yun', models.ForeignKey(blank=True, to='video.BaiduYun', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Youku',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('youku_video_id', models.CharField(max_length=50, blank=True)),
                ('title', models.CharField(help_text='\u89c6\u9891\u6807\u9898\uff0c\u80fd\u586b\u51992-50\u4e2a\u5b57\u7b26,\u4e0a\u4f20\u65f6\u5fc5\u9009', max_length=100, blank=True)),
                ('tags', models.TextField(help_text='\u4e0d\u8d85\u8fc710\u4e2a;\u5355\u4e2a\u6807\u7b7e\u6700\u5c112\u4e2a\u3001\u6700\u591a12\u4e2a\u5b57\u7b26;\u6807\u7b7e\u95f4\u7528\u82f1\u6587\u7684\u9017\u53f7(,)\u548c\u7a7a\u683c\u9694\u5f00\uff0c\u5355\u4e2atag\u4e2d\uff0c\u4e0d\u5141\u8bb8\u6709_ - ;\u5fc5\u9009', max_length=200, blank=True)),
                ('description', models.TextField(default='', help_text='\u89c6\u9891\u63cf\u8ff0\uff0c\u6700\u591a\u80fd\u51992000\u4e2a\u5b57', max_length=300, blank=True)),
                ('category', models.CharField(blank=True, max_length=50, choices=[('Games', '\u6e38\u620f'), ('Tech', '\u79d1\u6280'), ('News', '\u8d44\u8baf'), ('LifeStyle', '\u751f\u6d3b'), ('Original', '\u539f\u521b'), ('TV', '\u7535\u89c6\u5267'), ('Entertainment', '\u5a31\u4e50'), ('Movies', '\u7535\u5f71'), ('Sports', '\u4f53\u80b2'), ('Music', '\u97f3\u4e50'), ('Anime', '\u52a8\u6f2b'), ('Fashion', '\u65f6\u5c1a'), ('Parenting', '\u4eb2\u5b50'), ('Autos', '\u6c7d\u8f66'), ('Travel', '\u65c5\u6e38'), ('Education', '\u6559\u80b2'), ('Humor', '\u641e\u7b11'), ('Ads', '\u5e7f\u544a'), ('Others', '\u5176\u4ed6')])),
                ('published', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='YoukuPlaylist',
            fields=[
                ('id', models.CharField(max_length=8, serialize=False, primary_key=True)),
                ('duration', models.CharField(max_length=50, null=True, blank=True)),
                ('link', models.CharField(max_length=100, null=True, blank=True)),
                ('play_link', models.CharField(max_length=100, null=True, blank=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('video_count', models.CharField(max_length=10, null=True, blank=True)),
                ('view_count', models.CharField(max_length=10, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='YouTube',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vid_id', models.CharField(max_length=50)),
                ('vid_url', models.CharField(max_length=50)),
                ('playlist_url', models.URLField(max_length=300)),
                ('user', models.URLField(max_length=300)),
                ('keywords', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='YouTubeChannel',
            fields=[
                ('channel_id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500, blank=True)),
                ('thumbnail', models.URLField(max_length=300, blank=True)),
                ('is_download', models.NullBooleanField()),
                ('remark', models.CharField(max_length=50, blank=True)),
                ('category', models.ForeignKey(blank=True, to='video.Category', null=True)),
            ],
            options={
                'verbose_name': 'YouTube Channel',
                'verbose_name_plural': 'YouTube Channels',
            },
        ),
        migrations.CreateModel(
            name='YouTubePlaylist',
            fields=[
                ('playlist_id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500, blank=True)),
                ('thumbnail', models.URLField(max_length=300, blank=True)),
                ('publishedAt', models.DateTimeField(null=True, blank=True)),
                ('video_num', models.CharField(max_length=10, null=True, blank=True)),
                ('is_download', models.BooleanField(default=False)),
                ('remark', models.CharField(max_length=50, blank=True)),
                ('channel', models.ForeignKey(blank=True, to='video.YouTubeChannel', null=True)),
            ],
            options={
                'verbose_name': 'YouTube Playlist',
                'verbose_name_plural': 'YouTube Playlists',
            },
        ),
        migrations.AddField(
            model_name='youku',
            name='setted_youku_playlist',
            field=models.ForeignKey(related_name='setted_youku_playlist', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.YoukuPlaylist', help_text='\u8bbe\u7f6e\u8be5\u89c6\u9891\u6240\u5c5e\u7684Playlist', null=True),
        ),
        migrations.AddField(
            model_name='youku',
            name='video',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.Video'),
        ),
        migrations.AddField(
            model_name='youku',
            name='youku_playlist',
            field=models.ForeignKey(related_name='youku_playlist_online', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.YoukuPlaylist', help_text='\u8be5\u89c6\u9891\u5728\u4f18\u9177\u7f51\u4e0a\u5b9e\u9645\u4e0a\u7684Playlist', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='channel',
            field=models.ForeignKey(blank=True, to='video.YouTubeChannel', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='playlist',
            field=models.ForeignKey(blank=True, to='video.YouTubePlaylist', null=True),
        ),
        migrations.AddField(
            model_name='playlistconfig',
            name='youku_playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.YoukuPlaylist', help_text='\u8bbe\u7f6e\u89c6\u9891\u5728\u4f18\u9177\u7f51\u4e0a\u7684Playlist', null=True),
        ),
        migrations.AddField(
            model_name='playlistconfig',
            name='youtube_channel',
            field=models.ForeignKey(to='video.YouTubeChannel'),
        ),
        migrations.AddField(
            model_name='playlistconfig',
            name='youtube_playlist',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field='channel', to='video.YouTubePlaylist', chained_field='youtube_channel', show_all=True, auto_choose=True),
        ),
    ]
