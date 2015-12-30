# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20151219_0358'),
    ]

    operations = [
        migrations.CreateModel(
            name='YT_playlist',
            fields=[
                ('playlist_id', models.URLField(max_length=100, serialize=False, primary_key=True)),
                ('remark', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='video',
            name='id',
        ),
        migrations.RemoveField(
            model_name='video',
            name='url',
        ),
        migrations.AddField(
            model_name='video',
            name='description',
            field=models.CharField(max_length=300, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='file',
            field=models.FileField(null=True, upload_to='youtube', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='publishedAt',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=models.URLField(max_length=300, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='video_id',
            field=models.CharField(default=111, max_length=50, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='subtile_cn',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='subtile_en',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='title_cn',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
