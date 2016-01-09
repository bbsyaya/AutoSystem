# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0021_auto_20160107_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='channel',
            field=models.ForeignKey(blank=True, to='video.YT_channel', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='youku',
            name='description',
            field=models.TextField(default='', max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='yt_channel',
            name='category',
            field=models.ForeignKey(blank=True, to='video.category', null=True),
        ),
    ]
