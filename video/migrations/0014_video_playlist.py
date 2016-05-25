# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0013_auto_20160525_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='playlist',
            field=models.ForeignKey(blank=True, to='video.YouTubePlaylist', null=True),
        ),
    ]
