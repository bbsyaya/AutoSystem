# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0009_auto_20151230_2300'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='YT_channel',
            fields=[
                ('channel_id', models.URLField(max_length=100, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300, null=True, blank=True)),
                ('thumbnails', models.URLField(max_length=300, null=True, blank=True)),
                ('is_download', models.NullBooleanField()),
                ('remark', models.CharField(max_length=50)),
                ('category', models.ForeignKey(blank=True, to='video.category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
