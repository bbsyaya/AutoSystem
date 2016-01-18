# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0024_auto_20160116_0102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='subtile_cn',
            new_name='subtitle_cn',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='subtile_en',
            new_name='subtitle_en',
        ),
    ]
