# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0017_auto_20160107_1104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='youku',
            old_name='video_id',
            new_name='youku_video_id',
        ),
        migrations.RemoveField(
            model_name='video',
            name='youku',
        ),
        migrations.AddField(
            model_name='youku',
            name='youku',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='video.Video'),
            preserve_default=True,
        ),
    ]
