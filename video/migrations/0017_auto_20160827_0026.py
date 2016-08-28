# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0016_youkuplaylist_youtube_playlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youkuplaylist',
            name='youtube_playlist',
        ),
        migrations.AddField(
            model_name='youtubeplaylist',
            name='youku_playlist',
            field=models.ManyToManyField(to='video.YoukuPlaylist', null=True, blank=True),
        ),
    ]
