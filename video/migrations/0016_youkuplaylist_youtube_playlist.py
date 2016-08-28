# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0015_youtubeplaylist_video_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='youkuplaylist',
            name='youtube_playlist',
            field=models.ManyToManyField(to='video.YouTubePlaylist', null=True, blank=True),
        ),
    ]
