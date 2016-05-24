# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0012_youtubeplaylist_publishedat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='youtubeplaylist',
            old_name='youtube_channel',
            new_name='channel',
        ),
    ]
