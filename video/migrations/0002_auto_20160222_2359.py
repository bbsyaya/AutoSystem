# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='youku',
            name='setted_youku_playlist',
            field=models.ForeignKey(related_name='setted_youku_playlist', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.YoukuPlaylist', help_text='\u8bbe\u7f6e\u8be5\u89c6\u9891\u6240\u5c5e\u7684Playlist', null=True),
        ),
        migrations.AlterField(
            model_name='youku',
            name='youku_playlist',
            field=models.ForeignKey(related_name='youku_playlist_online', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.YoukuPlaylist', help_text='\u8be5\u89c6\u9891\u5728\u4f18\u9177\u7f51\u4e0a\u5b9e\u9645\u4e0a\u7684Playlist', null=True),
        ),
    ]
