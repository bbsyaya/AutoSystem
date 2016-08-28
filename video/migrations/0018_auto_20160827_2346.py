# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0017_auto_20160827_0026'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('youku_account', models.CharField(help_text='\u6307\u5b9a\u4e0a\u4f20\u5230\u4f18\u9177\u7684\u8d26\u53f7', max_length=100, blank=True)),
                ('is_enable', models.BooleanField()),
                ('remark', models.CharField(max_length=300, verbose_name='\u5907\u6ce8', blank=True)),
                ('youku_playlist', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.YoukuPlaylist', help_text='\u8bbe\u7f6e\u89c6\u9891\u5728\u4f18\u9177\u7f51\u4e0a\u7684Playlist', null=True)),
                ('youtube_channel', models.ForeignKey(to='video.YouTubeChannel')),
            ],
        ),
        migrations.RemoveField(
            model_name='videoconfig',
            name='youku_playlist',
        ),
        migrations.RemoveField(
            model_name='videoconfig',
            name='youtube_channel',
        ),
        migrations.RemoveField(
            model_name='videoconfig',
            name='youtube_playlist',
        ),
        migrations.RemoveField(
            model_name='youtubeplaylist',
            name='youku_playlist',
        ),
        migrations.DeleteModel(
            name='VideoConfig',
        ),
        migrations.AddField(
            model_name='playlistconfig',
            name='youtube_playlist',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field='channel', to='video.YouTubePlaylist', chained_field='youtube_channel', show_all=True, auto_choose=True),
        ),
    ]
