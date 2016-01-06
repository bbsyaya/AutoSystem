# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0013_auto_20160105_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='youku',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='youku',
            field=models.OneToOneField(null=True, blank=True, to='video.Youku'),
        ),
        migrations.AlterField(
            model_name='youku',
            name='video_id',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='yt_channel',
            name='category',
            field=models.ForeignKey(blank=True, to='video.category', null=True),
        ),
    ]
