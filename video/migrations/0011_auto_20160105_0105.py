# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0010_category_yt_channel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yt_channel',
            old_name='thumbnails',
            new_name='thumbnail',
        ),
    ]
