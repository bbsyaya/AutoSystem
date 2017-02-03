# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0022_auto_20170203_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubeplaylist',
            name='is_download',
            field=models.BooleanField(default=False),
        ),
    ]
