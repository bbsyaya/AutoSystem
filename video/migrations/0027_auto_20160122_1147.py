# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('video', '0026_auto_20160119_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='subtitle_merge',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='subtitle_video_file',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),

    ]
