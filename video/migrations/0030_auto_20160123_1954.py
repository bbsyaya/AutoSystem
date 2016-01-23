# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0029_auto_20160123_1944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youkuplaylist',
            name='youku',
        ),
        migrations.AddField(
            model_name='youku',
            name='youku_playlist',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.YoukuPlaylist'),
            preserve_default=True,
        ),
    ]
