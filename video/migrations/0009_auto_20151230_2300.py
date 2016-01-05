# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0008_merge'),
    ]

    operations = [
        migrations.DeleteModel(
            name='YT_playlist',
        ),
        migrations.RemoveField(
            model_name='youku',
            name='id',
        ),
        migrations.AddField(
            model_name='youku',
            name='category',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='youku',
            name='description',
            field=models.CharField(max_length=300, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='youku',
            name='published',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='youku',
            name='tags',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='youku',
            name='title',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='video',
            name='title_cn',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='youku',
            name='video_id',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
        ),
    ]
