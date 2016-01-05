# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0012_auto_20160105_0118'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='yt_channel',
            options={'verbose_name': 'YouTube Channel', 'verbose_name_plural': 'YouTube Channels'},
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='yt_channel',
            name='category',
            field=models.ForeignKey(blank=True, to='video.category', null=True),
        ),
    ]
