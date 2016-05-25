# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0014_video_playlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubeplaylist',
            name='video_num',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
