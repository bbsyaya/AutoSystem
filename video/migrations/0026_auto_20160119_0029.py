# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0025_auto_20160119_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='subtitle_cn',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='subtitle_en',
            field=models.CharField(max_length=100, blank=True),
        ),
        # migrations.AlterField(
        #     model_name='youku',
        #     name='youku_video_id',
        #     field=models.CharField(unique=True, max_length=50, blank=True),
        # ),
        # migrations.AlterField(
        #     model_name='yt_channel',
        #     name='category',
        #     field=models.ForeignKey(blank=True, to='video.Category', null=True),
        # ),
    ]
