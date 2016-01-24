# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0030_auto_20160123_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youku',
            name='youku_playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.YoukuPlaylist', null=True),
            preserve_default=True,
        ),
    ]
