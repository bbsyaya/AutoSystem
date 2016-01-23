# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0027_auto_20160122_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='YoukuPlaylist',
            fields=[
                ('id', models.CharField(max_length=8, serialize=False, primary_key=True)),
                ('duration', models.CharField(max_length=50, null=True, blank=True)),
                ('link', models.CharField(max_length=100, null=True, blank=True)),
                ('play_link', models.CharField(max_length=100, null=True, blank=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('video_count', models.CharField(max_length=10, null=True, blank=True)),
                ('view_count', models.CharField(max_length=10, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
