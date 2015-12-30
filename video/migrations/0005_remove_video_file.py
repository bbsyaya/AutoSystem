# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0004_delete_yt_playlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='file',
        ),
    ]
