# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0010_auto_20160524_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('youku_account', models.CharField(help_text='\u6307\u5b9a\u4e0a\u4f20\u5230\u4f18\u9177\u7684\u8d26\u53f7', max_length=100, blank=True)),
                ('is_enable', models.BooleanField()),
                ('remark', models.CharField(max_length=300, verbose_name='\u5907\u6ce8', blank=True)),
                ('youku_playlist', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.YoukuPlaylist', help_text='\u8bbe\u7f6e\u89c6\u9891\u5728\u4f18\u9177\u7f51\u4e0a\u7684Playlist', null=True)),
                ('youtube_channel', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.YouTubeChannel', help_text='\u6307\u5b9a\u4e0b\u8f7dyoutube\u4e0a\u7684\u6307\u5b9achannel', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='YouTubePlaylist',
            fields=[
                ('playlist_id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500, blank=True)),
                ('thumbnail', models.URLField(max_length=300, blank=True)),
                ('remark', models.CharField(max_length=50, blank=True)),
                ('youtube_channel', models.ForeignKey(blank=True, to='video.YouTubeChannel', null=True)),
            ],
            options={
                'verbose_name': 'YouTube Playlist',
                'verbose_name_plural': 'YouTube Playlists',
            },
        ),
        migrations.AddField(
            model_name='videoconfig',
            name='youtube_playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.YouTubePlaylist', help_text='\u6307\u5b9a\u4e0b\u8f7dyoutube channel\u91cc\u7684\u7279\u5b9aplaylist', null=True),
        ),
    ]
