# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0013_auto_20160105_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yt_channel',
            name='category',
            field=models.ForeignKey(blank=True, to='video.Category', null=True),
        ),
    ]
